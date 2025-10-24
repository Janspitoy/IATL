import numpy as np
from collections import Counter
import pandas as pd
import graphviz
import sys
import os

# --- Посилання на Graphviz (залиш це, воно працює) ---
graphviz_bin_path = r'C:\Users\Ivan\Graphviz-14.0.2-win64\bin'
if graphviz_bin_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + graphviz_bin_path


# --- Функції та Класи ---

def entropy(y):
    """Обчислює ентропію Шеннона."""
    y_int = y.astype(int)
    hist = np.bincount(y_int)
    ps = hist / len(y_int)
    return -np.sum([p * np.log2(p) for p in ps if p > 0])


class Node:
    """Клас для вузла дерева."""

    def __init__(self, feature=None, children=None, value=None):
        self.feature = feature
        self.children = children or {}
        self.value = int(value) if value is not None else None

    def is_leaf(self):
        return self.value is not None


# === ЗМІНА 1: Додаємо `max_depth` та `current_depth` ===
def build_tree(X, y, all_features_list, remaining_features, max_depth=None, current_depth=0):
    """Рекурсивна функція побудови дерева ID3 з обмеженням глибини."""

    # y вже є масивом int
    if len(np.unique(y)) == 1:
        return Node(value=y[0])

    if len(remaining_features) == 0:
        most_common_label = Counter(y).most_common(1)[0][0]
        return Node(value=most_common_label)

    # === ЗМІНА 2: НОВА УМОВА ЗУПИНКИ ===
    # Якщо ми досягли максимальної глибини, зупиняємось і повертаємо найчастіший клас
    if max_depth is not None and current_depth >= max_depth:
        most_common_label = Counter(y).most_common(1)[0][0]
        return Node(value=most_common_label)
    # ======================================

    gains = []
    for feat_name in remaining_features:
        col_idx = all_features_list.index(feat_name)
        values = np.unique(X[:, col_idx])
        gain = entropy(y)
        for val in values:
            sub_idx = (X[:, col_idx] == val)
            if np.sum(sub_idx) > 0:
                gain -= (np.sum(sub_idx) / len(y)) * entropy(y[sub_idx])
        gains.append(gain)

    best_gain_idx = np.argmax(gains)
    best_feat_name = remaining_features[best_gain_idx]

    node = Node(feature=best_feat_name)
    best_feat_col_idx = all_features_list.index(best_feat_name)
    new_remaining_feats = [f for f in remaining_features if f != best_feat_name]

    values = np.unique(X[:, best_feat_col_idx])
    for val in values:
        sub_idx = (X[:, best_feat_col_idx] == val)
        if np.sum(sub_idx) == 0:
            most_common_label = Counter(y).most_common(1)[0][0]
            node.children[val] = Node(value=most_common_label)
        else:
            # === ЗМІНА 3: Передаємо глибину в рекурсію ===
            node.children[val] = build_tree(
                X[sub_idx], y[sub_idx], all_features_list, new_remaining_feats,
                max_depth=max_depth, current_depth=current_depth + 1  # <-- Збільшуємо глибину
            )
    return node


# --- Функції print_tree та add_nodes_edges залишаються БЕЗ ЗМІН ---

def print_tree(node, indent="", labels=None):
    """Виводить дерево у текстовому форматі."""
    if node.is_leaf():
        key = node.value
        label = labels.get(key, f"Unknown(Key={key})")
        print(indent + "Leaf: " + label)
        return

    print(indent + "Node: " + node.feature)
    for val, child in node.children.items():
        print(indent + "  -> " + str(val) + ":")
        print_tree(child, indent + "    ", labels)


def add_nodes_edges(node, labels, graph, parent_id=None, edge_label=""):
    """Рекурсивний помічник для Graphviz."""
    node_id = str(id(node))
    if node.is_leaf():
        key = node.value
        label = labels.get(key, f"Unknown(Key={key})")
        graph.node(node_id, label=label, shape='box', style='filled', fillcolor='lightgreen')
    else:
        graph.node(node_id, label=node.feature, shape='ellipse', style='filled', fillcolor='lightblue')

    if parent_id:
        graph.edge(parent_id, node_id, label=edge_label)

    if not node.is_leaf():
        for val, child in node.children.items():
            add_nodes_edges(child, labels, graph, parent_id=node_id, edge_label=str(val))


# === Основний блок виконання ---

if __name__ == "__main__":

    dataset_filename = 'speech_translator_dataset_1500.csv'

    try:
        df = pd.read_csv(dataset_filename)
    except FileNotFoundError:
        print(f"ПОМИЛКА: Файл '{dataset_filename}' не знайдено.")
        sys.exit(1)

    all_features_list = ['Input_Language', 'Target_Language', 'Context', 'Sentence_Length']
    X = df[all_features_list].values

    unique_intents = np.unique(df['Intent'])
    intent_encoder = {val: idx for idx, val in enumerate(unique_intents)}
    intent_decoder = {idx: val for val, idx in intent_encoder.items()}
    y = np.array([intent_encoder[val] for val in df['Intent']], dtype=int)

    print(f"Завантажено {len(df)} записів з '{dataset_filename}'.")
    print("Кодування класів (Decoder):")
    print(intent_decoder)
    print("-" * 30)

    print("Починаю побудову дерева...")
    # === ЗМІНА 4: Встановлюємо максимальну глибину ===
    # Пограйся з цим числом. Почни з 2 або 3.
    MAX_TREE_DEPTH = 3

    tree = build_tree(X, y, all_features_list, all_features_list, max_depth=MAX_TREE_DEPTH)
    # ==================================================

    print(f"Побудова дерева завершена (max_depth={MAX_TREE_DEPTH}).")
    print("-" * 30)

    print("Побудоване дерево рішень (текстова версія):")
    print_tree(tree, labels=intent_decoder)
    print("-" * 30)

    print("Спроба візуалізації дерева...")
    try:
        dot = graphviz.Digraph(comment='Дерево рішень', format='png')
        dot.attr(fontsize='10')

        add_nodes_edges(tree, intent_decoder, dot)

        # Змінюємо ім'я файлу, щоб показати глибину
        output_filename = f'decision_tree_depth_{MAX_TREE_DEPTH}'
        dot.render(output_filename, view=True)

        print(f"\nВізуалізацію дерева збережено у файл '{output_filename}.png' і відкрито.")

    except Exception as e:
        print(f"\n[ПОМИЛКА ВІЗУАЛІЗАЦІЇ]: {e}")