import csv
import statistics
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
import plotly.express as px
import pandas as pd
from collections import Counter

import csv
import statistics
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
import plotly.express as px
import pandas as pd
from collections import Counter


#Cette fonction gère la visualisation interactive des données CSV. 
#Elle prend en charge plusieurs types de graphiques et permet de sélectionner des colonnes pour analyse.

def visualize_data(request):
    
    errors = []  # Liste des erreurs potentielles
    data = []  # Contient les données CSV
    headers = []  # Les en-têtes des colonnes du CSV

    # Gestion des fichiers : récupérer le dernier fichier téléversé
    fs = FileSystemStorage()
    filename = request.session.get('last_uploaded_file')  
    plot_type = request.GET.get('plot_type', 'histplot') 
    column_x = request.GET.get('column_x') 
    column_y = request.GET.get('column_y')  

    if filename and fs.exists(fs.path(filename)):
        # Charger le fichier CSV et extraire les données
        with open(fs.path(filename), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader, [])  # Lire les en-têtes
            for row in reader:
                data.append(row)

        # Créer un DataFrame Pandas pour analyse et visualisation
        df = pd.DataFrame(data, columns=headers)

        # Conversion des colonnes spécifiées en numérique
        for col in [column_x, column_y]:
            if col:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    errors.append(f"La colonne {col} ne peut pas être convertie en nombres.")

        # Génération des graphiques si les colonnes sont valides
        if column_x and column_y and not errors:
            template = 'plotly_white' 
            color_scheme = '#2563eb'  

            try:
                # Différents types de graphiques basés sur "plot_type"
                if plot_type == "histplot":
                    fig = px.histogram(df, x=column_x, title=f"Distribution de {column_x}", template=template,
                                       color_discrete_sequence=[color_scheme])
                elif plot_type == "barplot":
                    fig = px.bar(df, x=column_x, y=column_y, title=f"{column_y} par {column_x}", template=template,
                                 color_discrete_sequence=[color_scheme])
                elif plot_type == "scatterplot":
                    fig = px.scatter(df, x=column_x, y=column_y, title=f"Nuage de points {column_y} vs {column_x}",
                                     template=template, color_discrete_sequence=[color_scheme])
                elif plot_type == "boxplot":
                    fig = px.box(df, x=column_x, y=column_y, title=f"Boîte à moustaches de {column_y} par {column_x}",
                                 template=template, color_discrete_sequence=[color_scheme])
                elif plot_type == "violinplot":
                    fig = px.violin(df, x=column_x, title=f"Distribution de  {column_x}",
                                    template=template, color_discrete_sequence=[color_scheme])
                elif plot_type == "lineplot":
                    fig = px.line(df, x=column_x, y=column_y, title=f"Évolution de {column_y} en fonction de {column_x}",
                                  template=template, color_discrete_sequence=[color_scheme])
                elif plot_type == "heatmap":
                    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                    if column_x in numeric_cols and column_y in numeric_cols:
                        fig = px.density_heatmap(df, x=column_x, y=column_y,
                                                 title=f"Densité {column_y} vs {column_x}", template=template,
                                                 color_continuous_scale=['#FFB6C1', '#FFFACD', '#D8BFD8', '#ADD8E6'])
                    else:
                        errors.append("Les deux colonnes doivent être numériques pour une heatmap.")
                        fig = None
                elif plot_type == "countplot":
                    counts = df.groupby(column_x)[column_y].count().reset_index()
                    fig = px.bar(counts, x=column_x, y=column_y, title=f"Fréquence de {column_y} par {column_x}",
                                 template=template, color_discrete_sequence=[color_scheme])
                elif plot_type == "kdeplot":
                    fig = px.density_contour(df, x=column_x, y=column_y, title=f"Densité de {column_y} vs {column_x}",
                                             template=template, color_discrete_sequence=[color_scheme])
                else:
                    errors.append("Type de graphique non pris en charge.")
                    fig = None

                # Mise en page des graphiques
                if fig:
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_family="Poppins",
                        title_font_size=20,
                        title_x=0.5,
                        margin=dict(t=50, l=50, r=30, b=50),
                        showlegend=False
                    )
                    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)', zeroline=False,
                                     title_text=column_x)
                    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)', zeroline=False,
                                     title_text=column_y)

                    graph_html = fig.to_html(full_html=False, config={'displayModeBar': True, 'scrollZoom': True})
                else:
                    graph_html = None

            except Exception as e:
                errors.append(f"Erreur lors de la création du graphique : {str(e)}")
                graph_html = None

        else:
            errors.append("Veuillez sélectionner deux colonnes valides.")
            graph_html = None

        return render(request, 'csv_analyzer/visualization_page.html', {
            'graph_html': graph_html,
            'headers': headers,
            'errors': errors,
        })

    else:
        errors.append("Aucun fichier chargé. Veuillez charger un fichier CSV.")
        return render(request, 'csv_analyzer/upload_form.html', {'errors': errors})





def compare_columns(request):
    # Charger les données du CSV
    file_path = 'path/to/your/file.csv'  # Remplacez par le chemin correct
    df = pd.read_csv(file_path)

    # Récupérer les colonnes disponibles
    headers = df.columns.tolist()

    # Obtenir les colonnes sélectionnées par l'utilisateur
    column_x = request.GET.get('column_x')
    column_y = request.GET.get('column_y')

    # Analyse et comparaison des deux colonnes
    comparison_data = None
    if column_x and column_y:
        if column_x in df.columns and column_y in df.columns:
            # Vous pouvez adapter la logique de comparaison en fonction du type de données des colonnes
            comparison_data = {
                'correlation': df[column_x].corr(df[column_y]),
                'mean_x': df[column_x].mean(),
                'mean_y': df[column_y].mean(),
                # Ajoutez d'autres statistiques pertinentes selon vos besoins
            }

    return render(request, 'analysis_page.html', {
        'headers': headers,
        'selected_column_x': column_x,
        'selected_column_y': column_y,
        'comparison_data': comparison_data
    })


# 1. Fonction de upload du fichier csv

def upload_csv(request):
    errors = []
    headers = []
    data = []
    analysis_results = {}

    search_term = request.GET.get('search', '').strip().lower()
    line_number = request.GET.get('line', None)
    column_number = request.GET.get('column', None)

    if request.method == 'POST' and request.FILES.get('csv_file'):
        return handle_csv_upload(request, errors, headers, data)
    elif request.method == 'GET' and (search_term or 'page' in request.GET or line_number or column_number):
        fs = FileSystemStorage()
        filename = request.session.get('last_uploaded_file')
        if filename and fs.exists(fs.path(filename)):
            with open(fs.path(filename), 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader, [])
                for row in reader:
                    data.append(row)

            analysis_results = analyze_data(data, headers)

            filtered_data = [
                row for row in data if any(search_term in str(cell).lower() for cell in row)
            ] if search_term else data

            page_number = request.GET.get('page', 1)
            paginator = Paginator(filtered_data, 10)
            paginated_data = paginator.get_page(page_number)

            line_data = None
            if line_number:
                try:
                    line_number = int(line_number)
                    if 0 <= line_number < len(data):
                        line_data = data[line_number]
                    else:
                        errors.append("Numéro de ligne invalide.")
                except ValueError:
                    errors.append("Numéro de ligne invalide.")

            column_data = None
            if column_number:
                try:
                    column_number = int(column_number)
                    if 0 <= column_number < len(headers):
                        column_data = [row[column_number] for row in data]
                    else:
                        errors.append("Numéro de colonne invalide.")
                except ValueError:
                    errors.append("Numéro de colonne invalide.")

            return render(
                request,
                'csv_analyzer/upload_success.html',
                {
                    'data': paginated_data,
                    'headers': headers,
                    'errors': errors,
                    'search_term': search_term,
                    'line_data': line_data,
                    'column_data': column_data,
                    'line_number': line_number,
                    'column_number': column_number,
                    'analysis': analysis_results,
                },
            )
        else:
            errors.append("Aucun fichier chargé. Veuillez charger un fichier CSV.")
    return render(request, 'csv_analyzer/upload_form.html', {'errors': errors})



def upload_success(request):
    return render(request, 'csv_analyzer/upload_success.html')




def handle_csv_upload(request, errors, headers, data):
    csv_file = request.FILES['csv_file']
    fs = FileSystemStorage()
    filename = fs.save(csv_file.name, csv_file)

    request.session['last_uploaded_file'] = filename

    try:
        with open(fs.path(filename), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            try:
                headers = next(reader)
            except StopIteration:
                errors.append("Le fichier CSV est vide.")
                return render(request, 'csv_analyzer/upload_form.html', {'errors': errors})

            for row in reader:
                try:
                    data_row = [convert_cell(cell) for cell in row]
                except ValueError:
                    errors.append(f"Erreur de conversion dans la ligne : {row}")
                else:
                    data.append(data_row)

    except FileNotFoundError:
        errors.append("Fichier non trouvé.")
    except Exception as e:
        errors.append(f"Erreur lors du traitement du fichier : {e}")

    if errors:
        return render(request, 'csv_analyzer/upload_form.html', {'errors': errors})
    else:
        analysis_results = analyze_data(data, headers)

        page_number = request.GET.get('page', 1)
        paginator = Paginator(data, 10)
        paginated_data = paginator.get_page(page_number)

        return render(
            request,
            'csv_analyzer/upload_success.html',  # Redirection vers la page de succès
            {
                'data': paginated_data,
                'headers': headers,
                'analysis': analysis_results,
                'errors': errors,
                'search_term': '',
            },
        )






def analyze_csv(request):
    errors = []
    headers = []
    analysis_results = {}
    selected_column = request.GET.get('column')

    fs = FileSystemStorage()
    filename = request.session.get('last_uploaded_file')
    
    if filename and fs.exists(fs.path(filename)):
        with open(fs.path(filename), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader, [])
            data = list(reader)

        if selected_column:
            # Analyse uniquement la colonne sélectionnée
            col_index = headers.index(selected_column)
            column_data = [row[col_index] for row in data]
            analysis_results = analyze_data(data, headers, selected_column)
        
        return render(request, 'csv_analyzer/analysis_page.html', {
            'headers': headers,
            'selected_column': selected_column,
            'analysis': analysis_results,
            'errors': errors,
        })
    else:
        errors.append("Aucun fichier chargé. Veuillez charger un fichier CSV.")
        return render(request, 'csv_analyzer/upload_form.html', {'errors': errors})
    


def analyze_data(data, headers, selected_column=None):
    import statistics
    import math
    from collections import Counter
    
    def calculate_column_stats(column_data, is_numeric=True):
        if is_numeric:
            sorted_data = sorted(column_data)
            n = len(sorted_data)
            q1_pos = n // 4
            q3_pos = (3 * n) // 4
            
            mean = statistics.mean(column_data)
            variance = statistics.variance(column_data) if len(column_data) > 1 else 0
            
            # Calcul de l'asymétrie (skewness)
            if variance > 0:
                skewness = sum((x - mean) ** 3 for x in column_data) / ((n - 1) * math.pow(variance, 1.5))
            else:
                skewness = 0
                
            # Calcul du kurtosis
            if variance > 0:
                kurtosis = sum((x - mean) ** 4 for x in column_data) / ((n - 1) * variance ** 2) - 3
            else:
                kurtosis = 0
                
            # Détection des valeurs aberrantes
            q1 = sorted_data[q1_pos]
            q3 = sorted_data[q3_pos]
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = [x for x in column_data if x < lower_bound or x > upper_bound]
            
            return {
                "type": "numeric",
                "count": n,
                "mean": round(mean, 2),
                "median": round(statistics.median(column_data), 2),
                "mode": round(statistics.mode(column_data), 2) if len(set(column_data)) < n else None,
                "min": round(min(column_data), 2),
                "max": round(max(column_data), 2),
                "range": round(max(column_data) - min(column_data), 2),
                "variance": round(variance, 2),
                "stddev": round(math.sqrt(variance), 2) if variance > 0 else 0,
                "q1": round(q1, 2),
                "q3": round(q3, 2),
                "iqr": round(iqr, 2),
                "skewness": round(skewness, 2),
                "kurtosis": round(kurtosis, 2),
                "outliers_count": len(outliers),
                "outliers": [round(x, 2) for x in outliers[:10]],  # Limiter à 10 valeurs aberrantes
                "coefficient_variation": round((math.sqrt(variance) / mean) * 100, 2) if mean != 0 else 0
            }
        else:
            # Analyse pour données catégorielles
            value_counts = Counter(column_data)
            total = len(column_data)
            return {
                "type": "categorical",
                "count": total,
                "unique_count": len(value_counts),
                "mode": max(value_counts.items(), key=lambda x: x[1])[0],
                "frequencies": {k: {"count": v, "percentage": round((v/total)*100, 2)} 
                              for k, v in value_counts.most_common(10)},
                "entropy": round(-sum((v/total) * math.log2(v/total) 
                              for v in value_counts.values()), 2),
                "missing_values": column_data.count(''),
                "completeness": round((1 - column_data.count('')/total) * 100, 2)
            }

    analysis = {}
    
    if selected_column:
        # Analyse d'une seule colonne
        col_index = headers.index(selected_column)
        column_data = [row[col_index] for row in data]
        
        # Tentative de conversion en numérique
        try:
            numeric_data = [float(x) for x in column_data if x != '']
            if len(numeric_data) > 0:
                analysis[selected_column] = calculate_column_stats(numeric_data)
            else:
                analysis[selected_column] = calculate_column_stats(column_data, is_numeric=False)
        except ValueError:
            analysis[selected_column] = calculate_column_stats(column_data, is_numeric=False)
    else:
        # Analyse de toutes les colonnes (version simplifiée)
        for i, header in enumerate(headers):
            column_data = [row[i] for row in data]
            try:
                numeric_data = [float(x) for x in column_data if x != '']
                if len(numeric_data) > 0:
                    analysis[header] = calculate_column_stats(numeric_data)
                else:
                    analysis[header] = calculate_column_stats(column_data, is_numeric=False)
            except ValueError:
                analysis[header] = calculate_column_stats(column_data, is_numeric=False)
    
    return analysis

def convert_cell(cell):
    """ Convertit une cellule CSV en type approprié (int, float ou string) """
    try:
        return int(cell)
    except ValueError:
        try:
            return float(cell.replace(",", "."))
        except ValueError:
            return cell.strip()







