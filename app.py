
import pandas as pd
import re

# Lire le fichier CSV
df = pd.read_csv('traceforum.csv', sep=',', on_bad_lines='skip')

# Convertir les colonnes 'Date' et 'Heure' en DateTime
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Heure'], errors='coerce')

# Remplacer 'NULL' par NaT dans la colonne 'Delai' pour un traitement approprié
df['Delai'] = df['Delai'].replace('NULL', pd.NaT)

# Convertir la colonne 'Delai' en Timedelta
df['Delai'] = pd.to_timedelta(df['Delai'], errors='coerce')

# Extraire 'IDParent' et 'IDForum' depuis la colonne 'Attribut'
df['IDParent'] = df['Attribut'].apply(
    lambda x: re.search(r'IDParent=(\d+)', x).group(1) if re.search(r'IDParent=(\d+)', x) else None
)
df['IDForum'] = df['Attribut'].apply(
    lambda x: re.search(r'IDForum=(\d+)', x).group(1) if re.search(r'IDForum=(\d+)', x) else None
)

# Exclure les actions de connexion
actions_a_exclure = ['Connexion']
data_filtre = df[~df['Titre'].isin(actions_a_exclure)].copy()

# Seuil d'inactivité de 30 minutes
inactivity_threshold = pd.Timedelta(minutes=30)

# Dictionnaire pour les comptages des actions dans chaque forum
forum_counts = {}

# Ouvrir le fichier CSV en mode lecture
with open('traceforum.csv', 'r', encoding='utf-8') as file:
    for line in file:
        if "Répondre à un message" in line or "Poster un nouveau message" in line:
            match = re.search(r'IDForum=(\d+)', line)
            if match:
                forum_id = match.group(1)
                if forum_id not in forum_counts:
                    forum_counts[forum_id] = {'Répondre à un message': 0, 'Poster un nouveau message': 0}
                if "Répondre à un message" in line:
                    forum_counts[forum_id]['Répondre à un message'] += 1
                if "Poster un nouveau message" in line:
                    forum_counts[forum_id]['Poster un nouveau message'] += 1

# Fonction de comparaison des statistiques et calcul des pourcentages par rapport aux valeurs maximales
def comparer_stats(forum_counts, data_filtre):
    max_total_interaction_time = pd.Timedelta(0)
    max_user_interaction_time = pd.Timedelta(0)
    max_average_interactions_percentage = 0
    max_leaders_count = 0
    max_reactives_count = 0
    forum_max_stats = {}

    for forum_id, data in data_filtre.groupby('IDForum'):
        data = data.sort_values(by='DateTime').reset_index(drop=True)
        total_interaction_time = pd.Timedelta(0)
        for i in range(1, data.shape[0]):
            time_diff = data['DateTime'].iloc[i] - data['DateTime'].iloc[i - 1]
            if time_diff <= inactivity_threshold:
                total_interaction_time += time_diff

        total_interaction_time += data['Delai'][data['Delai'] <= inactivity_threshold].sum()
        data['TimeDiff'] = data['DateTime'].diff().fillna(pd.Timedelta(0))
        data['InteractionTime'] = data['TimeDiff'] + data['Delai'].fillna(pd.Timedelta(0))

        data_filtered = data[data['TimeDiff'] <= inactivity_threshold]
        mean_interaction_time = data_filtered.groupby('Utilisateur')['InteractionTime'].mean()
        user_interaction_time = mean_interaction_time.mean() if not mean_interaction_time.empty else pd.Timedelta(0)

        counts = forum_counts.get(forum_id, {'Répondre à un message': 0, 'Poster un nouveau message': 0})
        if counts['Poster un nouveau message'] > 0:
            if counts['Poster un nouveau message'] > counts['Répondre à un message']:
                average_interactions_percentage = (counts['Répondre à un message'] / counts['Poster un nouveau message']) * 100
            else:
                average_interactions_percentage = (counts['Poster un nouveau message'] / counts['Répondre à un message']) * 100
        else:
            average_interactions_percentage = 0

        relances = data[data['IDParent'].isna()]
        relances_par_utilisateur = relances['Utilisateur'].value_counts()
        total_relances = relances.shape[0]
        leaders = [utilisateur for utilisateur, count in relances_par_utilisateur.items() if count >= 0.1 * total_relances]
        users_reactifs = data['Utilisateur'].value_counts()
        users_reactifs_10_plus = users_reactifs[users_reactifs > 10]

        forum_max_stats[forum_id] = {
            'Total Interaction Time': total_interaction_time,
            'User Interaction Time': user_interaction_time,
            'Average Interactions Percentage': average_interactions_percentage,
            'Leaders Count': len(leaders),
            'Reactives Count': len(users_reactifs_10_plus)
        }

        max_total_interaction_time = max(max_total_interaction_time, total_interaction_time)
        max_user_interaction_time = max(max_user_interaction_time, user_interaction_time)
        max_average_interactions_percentage = max(max_average_interactions_percentage, average_interactions_percentage)
        max_leaders_count = max(max_leaders_count, len(leaders))
        max_reactives_count = max(max_reactives_count, len(users_reactifs_10_plus))

    # Liste pour sauvegarder les statistiques en CSV
    forum_stats_list = []

    # Calcul des pourcentages et ajout à la liste
    for forum_id, stats in forum_max_stats.items():
        total_interaction_time_percentage = (stats['Total Interaction Time'] / max_total_interaction_time) * 100 if max_total_interaction_time > pd.Timedelta(0) else 0
        user_interaction_time_percentage = (stats['User Interaction Time'] / max_user_interaction_time) * 100 if max_user_interaction_time > pd.Timedelta(0) else 0
        average_interactions_percentage = (stats['Average Interactions Percentage'] / max_average_interactions_percentage) * 100 if max_average_interactions_percentage > 0 else 0
        leaders_percentage = (stats['Leaders Count'] / max_leaders_count) * 100 if max_leaders_count > 0 else 0
        reactives_percentage = (stats['Reactives Count'] / max_reactives_count) * 100 if max_reactives_count > 0 else 0

        qualité = (total_interaction_time_percentage + user_interaction_time_percentage + average_interactions_percentage +
                   leaders_percentage + reactives_percentage) / 5

        forum_stats_list.append({
            'Forum ID': forum_id,
            'Total Interaction Time (%)': round(total_interaction_time_percentage, 2),
            'User Interaction Time (%)': round(user_interaction_time_percentage, 2),
            'Average Interactions Percentage (%)': round(average_interactions_percentage, 2),
            'Leaders Count (%)': round(leaders_percentage, 2),
            'Reactives Count (%)': round(reactives_percentage, 2),
            'Quality Score (%)': round(qualité, 2)
        })

    # Sauvegarder les statistiques dans un fichier CSV
    stats_df = pd.DataFrame(forum_stats_list)
    stats_df.to_csv('forum_stats.csv', index=False)
    print("Les pourcentages des statistiques ont été sauvegardés dans 'forum_stats.csv'.")

# Appeler la fonction de comparaison et de sauvegarde des statistiques
comparer_stats(forum_counts, data_filtre)
