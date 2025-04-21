# Synthetic CXM Generator

Generador de datasets sintéticos para simulación de interacciones multicanal en entornos de Customer Experience Management (CXM), con capacidad de inyectar anomalías configurables y generar escenarios específicos para entrenamiento y validación de modelos de detección de anomalías.

## 🚀 Características principales

- Generación de interacciones sintéticas en múltiples canales (ej. llamadas, chats, emails, etc.)
- Perfiles de comportamiento derivados de datasets reales (probabilísticos y estructurales)
- Inyección controlada de anomalías (temporales, estructurales, distribucionales, etc.)
- Arquitectura modular y extensible
- Salida en formato estructurado (`.csv`, `.json`) para fácil integración con modelos ML

## 🧱 Estructura del Proyecto

```text
synthetic-cxm-generator/
├── generator/            # Lógica del generador y módulos por canal
│   ├── base_generator.py
│   ├── channel_simulator.py
│   ├── anomaly_injector.py
│   └── scenario_builder.py
├── config/               # Configuraciones YAML para escenarios
│   └── generator_config.yaml
├── data_profiles/        # Perfiles de comportamiento real/sintético
│   └── profile_base.json
├── datasets/             # Datasets generados (output)
├── tests/                # Tests unitarios
│   └── test_generator.py
├── utils/                # Utilidades comunes (logs, validadores)
│   └── logger.py
├── main.py               # Script principal de ejecución
├── requirements.txt      # Dependencias
└── README.md             # Este archivo
```text

## ⚙️ Instalación

```bash
# Clona el repositorio
git clone https://github.com/adrodriguezlopez/synthetic-cxm-generator.git
cd synthetic-cxm-generator

# Crea y activa entorno virtual
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate

# Instala dependencias
pip install -r requirements.txt

## ▶️ Uso básico
python main.py --config config/generator_config.yaml
📌 Este comando generará un dataset sintético dentro de la carpeta /datasets con base en el escenario configurado.

Pronto se incluirán notebooks y ejemplos para exploración y visualización.

🧪 Estado actual
🔧 En desarrollo inicial: se está implementando el módulo base del generador y la simulación de canales. El sistema ya está integrado con Git y listo para extenderse.

🧭 Próximos pasos
Implementación de base_generator.py y channel_simulator.py

Incorporación de perfiles de datos reales

Interfaz básica para configurar escenarios desde CLI

Scripts de visualización y análisis exploratorio