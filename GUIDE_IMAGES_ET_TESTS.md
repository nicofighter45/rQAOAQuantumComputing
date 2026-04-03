# GUIDE: Images pour le Rapport RQAOA

## Vue d'Ensemble
Ce guide indique précisément quelles images générer, comment les nommer, et où les insérer dans le rapport LaTeX.

---

## Images à Insérer (5 Graphiques)

### 1. **results_boxplot.png** (PRIORITÉ HAUTE)
**Description**: Distributions des ratios d'approximation par type de graphe

**Où l'insérer**: Figure 1 (Section 4.2.2)
**Référence LaTeX**: Figure~\ref{fig:boxplot}
**Ce qu'il montre**:
- Box plot montrant la médiane, quartiles et outliers
- Permet de voir la variabilité des résultats pour chaque type de graphe
- La ligne rouge (ratio = 1.0) marque la performance optimale
- Important pour comparer les topologies de graphes

**Code d'insertion**:
```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.9\linewidth]{results_boxplot.png}
\caption{Distribution of RQAOA approximation ratios by graph type...}
\label{fig:boxplot}
\end{figure}
```

---

### 2. **results_barplot_with_errors.png** (PRIORITÉ HAUTE)
**Description**: Ratios moyens avec barres d'erreur (écarts-types)

**Où l'insérer**: Figure 2 (Section 4.2.2)
**Référence LaTeX**: Figure~\ref{fig:barplot}
**Ce qu'il montre**:
- Hauteur des barres = ratio moyenne pour chaque graphe
- Barres d'erreur = écart-type (variation dans les 10 runs)
- Valeurs numériques affichées au sommet des barres
- Permet une lecture quantitative rapide

**Ordre recommandé**: Placer APRÈS le boxplot pour plus de détails

---

### 3. **results_histogram.png** (PRIORITÉ HAUTE)
**Description**: Distribution globale des 90 ratios d'approximation

**Où l'insérer**: Figure 3 (Section 4.2.3)
**Référence LaTeX**: Figure~\ref{fig:histogram}
**Ce qu'il montre**:
- Histogramme (bins=30) de tous les ratios
- Lignes verticales: moyenne (rouge), médiane (vert), optimal=1.0 (orange)
- Révèle la type de distribution (symétrique, asymétrique, multimodale)
- Utile pour décrire le comportement global

---

### 4. **results_scatter_costs.png** (PRIORITÉ MOYENNE)
**Description**: Comparaison coûts optimaux vs estimés

**Où l'insérer**: Figure 4 (Section 4.2.4)
**Référence LaTeX**: Figure~\ref{fig:scatter}
**Ce qu'il montre**:
- Chaque point = une exécution (90 points total)
- Axe X = coûts optimaux (brute-force)
- Axe Y = coûts estimés (RQAOA)
- Ligne rouge (y=x) = performance parfaite
- Colormap indique les ratios d'approximation
- Points proches de la diagonale = bon performance

**Points importants à mentionner**:
- Tous les points doivent être AU-DESSUS de la diagonale (RQAOA ≤ Optimal)
- La proximité à y=x reflète la qualité de la solution

---

### 5. **results_summary_table.png** (PRIORITÉ HAUTE)
**Description**: Tableau récapitulatif des statistiques

**Où l'insérer**: Figure 5 (Section 4.3)
**Référence LaTeX**: Table~\ref{tab:results_summary}
**Contient pour chaque graphe**:
- Nom du graphe
- Ratio moyen
- Écart-type
- Ratio min et max
- Nombre de samples

**Format idéal**: Tableau avec alternance de couleurs (gris/blanc)
- En-têtes en gris foncé avec texte blanc
- Dernière ligne (GLOBAL) en vert clair
- Police = 10pt minimum (lisible dans le rapport)

---

## Instructions de Nommage et Rangement

### Dossier de destination recommandé:
```
rQAOAQuantumComputing/
├── rapport/
│   ├── figures/
│   │   ├── results_boxplot.png
│   │   ├── results_barplot_with_errors.png
│   │   ├── results_histogram.png
│   │   ├── results_scatter_costs.png
│   │   └── results_summary_table.png
│   └── main.tex
```

### Exporter depuis Jupyter (code à ajouter):
```python
# Après chaque graphique, ajouter:
plt.savefig('path/to/results_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
```

---

## Tests Supplémentaires: Autres Graphes

Pour enrichir votre analyse, testez les graphes suivants:

### **Set 1: Graphes Aléatoires (Déjà en place)**
- ✅ Erdős-Rényi (n=8,12,16; p=0.4,0.6,0.8)

### **Set 2: Graphes Reguliers (À AJOUTER)**
```python
# Décommenter dans la cellule 42:
RANDOM_REGULAR_GRAPHS = {
    '2-Regular(n=8)': nx.random_regular_graph(2, 8),
    '2-Regular(n=12)': nx.random_regular_graph(2, 12),
    '2-Regular(n=16)': nx.random_regular_graph(2, 16),
    '3-Regular(n=8)': nx.random_regular_graph(3, 8),
    '3-Regular(n=12)': nx.random_regular_graph(3, 12),
    '3-Regular(n=16)': nx.random_regular_graph(3, 16),
}
```

### **Set 3: Graphes Complets**
```python
COMPLETE_GRAPHS = {
    'K_8': nx.complete_graph(8),
    'K_12': nx.complete_graph(12),
    'K_16': nx.complete_graph(16),
}
```
**Intérêt**: Borne supérieure théorique; tous les nœuds maximalement connectés

### **Set 4: Grid 2D (Topologie Hardware)**
```python
GRID_2D_GRAPHS = {
    'Grid(2x4)': nx.grid_2d_graph(2, 4),
    'Grid(3x4)': nx.grid_2d_graph(3, 4),
    'Grid(4x4)': nx.grid_2d_graph(4, 4),
}
```
**Intérêt**: Simule les qubits arrangés sur puce

### **Set 5: Graphes Bipartites Complets**
```python
COMPLETE_BIPARTITE_GRAPHS = {
    'K_{4,4}': nx.complete_bipartite_graph(4, 4),
    'K_{6,6}': nx.complete_bipartite_graph(6, 6),
    'K_{8,8}': nx.complete_bipartite_graph(8, 8),
}
```
**Intérêt**: Cas dégénéré où la solution optimale est triviale (tous les nœuds d'un côté vs l'autre)

### **Set 6: Chemins et Échelles**
```python
PATH_GRAPHS = {
    'Path(8)': nx.path_graph(8),
    'Path(12)': nx.path_graph(12),
    'Path(16)': nx.path_graph(16),
}

LADDER_GRAPHS = {
    'Ladder(4)': nx.ladder_graph(4),
    'Ladder(6)': nx.ladder_graph(6),
    'Ladder(8)': nx.ladder_graph(8),
}
```
**Intérêt**: Structures linéaires et quasi-linéaires

---

## Code pour Tester Plusieurs Sets de Graphes

### Modification de la cellule 42:

```python
rnd.seed(seed)
np.random.seed(seed)

# Construire progressivement les graphes à tester
ALL_GRAPHS = {}

# Set 1: Erdős-Rényi (déjà implémenté)
ALL_GRAPHS.update(ERDOS_RENYI_GRAPHS)

# Set 2: Graphes réguliers
ALL_GRAPHS.update(RANDOM_REGULAR_GRAPHS)

# Set 3: Graphes complets
ALL_GRAPHS.update(COMPLETE_GRAPHS)

# Set 4: Grids 2D
ALL_GRAPHS.update(GRID_2D_GRAPHS)

# Set 5: Bipartites
ALL_GRAPHS.update(COMPLETE_BIPARTITE_GRAPHS)

# Set 6: Chemins et échelles
ALL_GRAPHS.update(PATH_GRAPHS)
ALL_GRAPHS.update(LADDER_GRAPHS)

print(f"Total graph instances to test: {len(ALL_GRAPHS)}")
```

---

## Stratégie Recommandée de Tests Progressifs

### **Phase 1: Validation (Actuel)**
- ✅ Erdős-Rényi seulement (9 graphes, 90 echantillons)
- Temps: ~1-2 heures
- Graphiques générés

### **Phase 2: Expansion (Recommandé)**
- ➕ Ajouter Graphes Réguliers et Complets
- Total: 15 graphes (150 samples)
- Temps: ~2-3 heures
- Fournit une belle section de résultats

### **Phase 3: Analyse Approfondie (Optionnel)**
- ➕ Ajouter Grids 2D, Bipartites, Chemins
- Total: 24 graphes (240 samples)
- Temps: ~4-6 heures
- Résultats très complets
- Permet d'étudier l'impact de la structure

---

## Métriques Clés à Rapporter

Pour chaque ensemble de résultats, incluez obligatoirement:

1. **Nombre total de samples**: (e.g., 90 pour Erdős-Rényi)
2. **Ratio d'approximation moyen**: (calculé automatiquement)
3. **Déviation standard**: (variabilité)
4. **Meilleure et pire performance**: Min/Max
5. **Médiane**: Plus robuste que la moyenne aux outliers

Format texte pour le rapport:
```
"Across all 90 test instances, RQAOA achieved a mean approximation 
ratio of X.XXX ± 0.XXX (mean ± std), with minimum and maximum 
ratios of X.XXX and X.XXX respectively."
```

---

## Checklist pour la Génération Finale

- [ ] Exécuter toutes les cellules de visualisation
- [ ] Exporter les 5 graphiques en PNG (dpi=300)
- [ ] Vérifier que les noms de fichiers correspondent exactement
- [ ] Placer dans dossier `rapport/figures/`
- [ ] Tester la compilation LaTeX avec \includegraphics
- [ ] Ajuster les largeurs (\linewidth) si nécessaire
- [ ] Vérifier que les légendes sont lisibles dans le rapport
- [ ] Optionnel: Ajouter plus de graphes selon Phase 2/3

---

## Format LaTeX Minimal pour le Rapport

```latex
\documentclass{article}
\usepackage{graphicx}
\usepackage{booktabs}

\graphicspath{{figures/}}

\begin{document}

\input{RESULTS_SECTION.tex}

\end{document}
```

Compilez avec:
```bash
pdflatex -interaction=nonstopmode rapport.tex
```
