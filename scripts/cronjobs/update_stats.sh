#!/bin/bash

echo "🔄 Mise à jour des tirages et des statistiques..."
python scripts/add_new_draws.py
python scripts/analyze_stats.py
echo "✅ Mise à jour terminée."
chmod +x cronjobs/update_stats.sh
