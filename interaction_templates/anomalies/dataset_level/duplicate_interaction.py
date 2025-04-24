import pandas as pd
import random
from interaction_templates.anomalies.base_anomaly import BaseAnomaly

class DatasetDuplicateInteractionAnomaly(BaseAnomaly):
    category = "dataset"

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Selects a random interaction from the dataset and duplicates it
        (including its original interaction_id). This simulates data duplication
        at the ingestion or replication level.
        """
        if df.empty:
            return df
        
        #group by interaction_id
        grouped = df.groupby("interaction_id")
        interaction_ids = list(grouped.groups.keys())

        if not interaction_ids:
            return df
        
        # Pick a random interaction_id
        selected_id = random.choice(interaction_ids)
        duplicated_df = grouped.get_group(selected_id).copy()

        return pd.concat([df, duplicated_df], ignore_index=True)
