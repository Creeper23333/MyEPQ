"""Lightweight in-repo random forest regressor."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np

from epq_pipeline.config import RandomForestConfig


@dataclass
class TreeNode:
    prediction: float
    feature_index: int | None = None
    threshold: float | None = None
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


class SimpleRandomForestRegressor:
    def __init__(self, config: RandomForestConfig, random_state: int) -> None:
        self.config = config
        self.random_state = random_state
        self.trees: list[TreeNode] = []
        self.feature_importances_: np.ndarray | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> "SimpleRandomForestRegressor":
        rng = np.random.default_rng(self.random_state)
        n_samples, n_features = x.shape
        max_features = self.config.max_features or max(1, int(math.sqrt(n_features)))
        importances = np.zeros(n_features, dtype=float)
        self.trees = []
        for _ in range(self.config.n_estimators):
            sample_idx = rng.integers(0, n_samples, size=n_samples)
            tree = self._build_tree(x[sample_idx], y[sample_idx], 0, rng, max_features, importances)
            self.trees.append(tree)
        total = float(importances.sum())
        self.feature_importances_ = importances / total if total > 0 else importances
        return self

    def _build_tree(
        self,
        x: np.ndarray,
        y: np.ndarray,
        depth: int,
        rng: np.random.Generator,
        max_features: int,
        importances: np.ndarray,
    ) -> TreeNode:
        prediction = float(np.mean(y))
        if (
            depth >= self.config.max_depth
            or len(y) < 2 * self.config.min_samples_leaf
            or float(np.var(y)) < 1e-12
        ):
            return TreeNode(prediction=prediction)

        n_features = x.shape[1]
        feature_indices = rng.choice(n_features, size=max_features, replace=False)
        parent_sse = float(np.sum((y - prediction) ** 2))
        best: dict[str, Any] | None = None

        for feature_index in feature_indices:
            values = x[:, feature_index]
            thresholds = np.unique(np.quantile(values, np.linspace(0.10, 0.90, 9)))
            for threshold in thresholds:
                left_mask = values <= threshold
                left_count = int(left_mask.sum())
                right_count = len(y) - left_count
                if left_count < self.config.min_samples_leaf or right_count < self.config.min_samples_leaf:
                    continue
                left_y = y[left_mask]
                right_y = y[~left_mask]
                left_sse = float(np.sum((left_y - np.mean(left_y)) ** 2))
                right_sse = float(np.sum((right_y - np.mean(right_y)) ** 2))
                gain = parent_sse - left_sse - right_sse
                if gain > 1e-14 and (best is None or gain > best["gain"]):
                    best = {
                        "feature_index": int(feature_index),
                        "threshold": float(threshold),
                        "left_mask": left_mask,
                        "gain": gain,
                    }

        if best is None:
            return TreeNode(prediction=prediction)

        importances[best["feature_index"]] += best["gain"]
        left_mask = best["left_mask"]
        return TreeNode(
            prediction=prediction,
            feature_index=best["feature_index"],
            threshold=best["threshold"],
            left=self._build_tree(x[left_mask], y[left_mask], depth + 1, rng, max_features, importances),
            right=self._build_tree(x[~left_mask], y[~left_mask], depth + 1, rng, max_features, importances),
        )

    def predict(self, x: np.ndarray) -> np.ndarray:
        if not self.trees:
            raise ValueError("Model has not been fitted")
        predictions = np.column_stack([self._predict_tree(tree, x) for tree in self.trees])
        return np.clip(predictions.mean(axis=1), 0.0, None)

    def _predict_tree(self, tree: TreeNode, x: np.ndarray) -> np.ndarray:
        return np.array([self._predict_one(tree, row) for row in x], dtype=float)

    def _predict_one(self, node: TreeNode, row: np.ndarray) -> float:
        while node.feature_index is not None and node.threshold is not None:
            if row[node.feature_index] <= node.threshold:
                node = node.left or node
            else:
                node = node.right or node
        return node.prediction

