from datetime import datetime
from dataset_builder.default_batch_generator import DefaultBatchGenerator

schema = [
    {"channel":"call", "interaction_type": "call_transfer", "count": 10},
    {"channel": "chat", "interaction_type": "standard", "count": 5}
]

generator = DefaultBatchGenerator(
    cxm="CXM1",
    apply_anomalies=True,
    anomaly_config_path="config/anomaly_profiles/test_profile.yaml"
)

df = generator.generate(
    schema=schema,
    base_timestamp=datetime.utcnow(),
    interaction_spacing_seconds=10
)

generator.export("datasets/generated_output.csv", format="json")

metrics = generator.get_anomaly_metrics()
print("\nBatch generation complete!")
print("Anomlay metrics:")
for k,v in metrics.items():
    print(f"{k}: {v}")