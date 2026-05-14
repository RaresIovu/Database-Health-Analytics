# Database Health Analytics

A real-time monitoring and analysis suite that combines local system telemetry with **AI-driven behavioral insights**. This project was developed to provide a view into database server and machine health, using automated metric collection.

## Setup & Installation

1. **Prerequisites**

Before setting up the virtual environment, ensure the following are installed:

* Python 3.9+ (Required for genai and threading features)

* PostgreSQL 15+ (The database engine)

* A Google Cloud Console Project (To obtain your Gemini API Key)

Database Initialization: Once PostgreSQL is running, the system will automatically attempt to create the required tables on the first run using the initialization scripts found in /database.

2. **Environment:**

Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv\Scripts\Activate.ps1
pip install -r requirements.txt

```


3. **Configuration:**

Create a `.env` file in the root directory:
```env
DB_PASSWORD = your_pwd_here
DB_NAME = db_name_here
HOST = address_here
PORT = port_here
API_KEY = your_api_key_here

```
By using a .env file, portability is provided to the database health system. Also prevents the accidental exposure of sensitive credentials in version control.

4. **Execution:**

```bash
python app.py

```

## Dependencies

The following packages are required for the system environment:

1. **Flask** Lightweight WSGI web application framework. Includes Jinja2
2. **psycopg2-binary** For establishing the connection to the database, and to send queries to it
3. **psutil** To gather system metrics such as CPU, RAM usage, along with disk and swap memory
4. **dotenv** To draw data from the .env file, allowing portability
5. **genai** For the gemini API requests used for AI insights

---
## Other Libraries Used

1. **os** For filepath managing, getenv.
2. **json** For storing metrics in JSON format, easy to be parsed. It is also the input for the AI client. Although it has a higher token usage, LLMs are better trained on this format. Theres also no need for manual mapping
3. **time** For time.sleep(), used in metric collecting
4. **random** Used to randomly send SELECT pg_sleep() queries to the database
5. **threading** For the creation of more threads, used by the collector and traffic simulator
6. **queue** For the queue data type, used in the simulation manager
7. **datetime** For the addition of timestamps to logs
---

## Key Features

* **Dual-Layer Monitoring:** Captures both low-level system metrics (CPU, RAM, Disk) and high-level DB performance (Latency, Connection Pools, Slow Queries).
* **Gemini AI Integration:** Uses Gemini 2.5 Flash to analyze batches of 10 snapshots, transforming JSON metrics into human-readable stability reports.
* **Persistence:** Implemented a JSON-based storage system in the `/data` directory that survives server restarts.
* **Interactive Controls:** Includes a built-in stress-test simulator to validate monitoring alerts and AI detection capabilities.

---



## Project Structure

```text
├── app.py               # Running this opens the Flask server
├── collector.py         # Background metric gathering. This runs in a separate thread
├── metrics/             # Contains the methods for DB and System metric collecting
├── data/                # Persistent JSON storage (Ignored by Git)
|   ├── ai_insights.json # A list of AI reports given based on the db log
|   └── db_log.json      # Contains various metrics about system and database
├── ai_handler.py        # Gemini API integration
├── tests/               # Contains the simulation manager and query methods. Runs in a separate thread. Listens to start/stop commands. Also contains a few batch scripts.
├── routes/              # Where API methods live. These are called from the frontend
├── database/            # Handles initialization of the database and its tables. Also provides a getter method for a connection
├── templates/           # Jinja2 HTML templates (Dashboard, Reports, AI)
├── json_service.py      # JSON save/load methods are defined here
├── requirements.txt     # The dependencies. Install via pip
└── .env                 # API Keys and Database credentials(Also ignored by Git)




```
* **Note for ai_handler.py:** The generate_answer method contains a try/except block, which sends a user-friendly "Server is under high traffic" message. I am not sure if this particular scenario sends an exception, or if the output is inside `response.text`. So far this has not happened. Unfortunately it is also out of my control since this depends on gemini servers. 
Furthermore, I was not able to test the output in the case of having reached the daily request limit.
---



## Design Decisions & Optimization

1. **Modularization**
The project is decoupled into dedicated modules (metrics/, database/, tests/) to ensure the Single Responsibility Principle.

database/: Instead of opening connections haphazardly, I implemented a custom Database Context Manager wrapper. This ensures that every connection is automatically pooled or closed correctly, preventing "Too many clients" errors.

routes/ vs app.py: By moving API logic into a separate routes/ directory, the core server remains lightweight and easier to debug.

2. **Simulation Manager** (Command-Response Pattern)
The Stress Test system is effectively a Simulation Manager that runs on its own thread.

It utilizes a queue.Queue to listen for START or STOP commands from the frontend.

This allows the user to trigger database behaviors (like pg_sleep injections) without freezing the main Flask application.

3. **Dynamic Templating with Jinja2**
Rather than serving static files, the frontend uses Jinja2 to perform server-side logic:

Page highlighting in the nav-bar: Navigation links apply the .activ class based on the current route.

Parametrised HTML: Data are passed as arguments in render_template() and used to dynamically modify the html based on it, which is then rendered

Threshold Logic: The UI performs real-time evaluation of metrics to switch between STABLE and CRITICAL badges without requiring extra JavaScript overhead.

4. **Graceful Resiliency & Error Handling**
Try-Except blocks: Multiple methods include a try/except wrapper to catch exceptions, returning an error message instead of crashing the server. This is used, for example, by the db connection getter, which automatically performs a roll-back in case of an exception

Timeout-Based Threading: Background workers use queue.get(timeout=1) to prevent "zombie threads," ensuring the application shuts down cleanly when the main process is terminated.

5. **Custom Database Context Manager**
Instead of manual connection handling, I implemented a custom `@contextmanager` decorator. This architectural choice:
* Guarantees the connection is closed even if the underlying query fails, preventing memory leaks.
* Reduces boilerplate code across modules which use database querying.

6. **Portability**
By using an .env file for the database credential and API key, the migration between one database to another is seamless, as the user just needs to redefine the parameters. Also prevents sensitive data from being commited to public repositories(If .env is ignored)
---

## The Website

The server also provides frontend endpoints, defined by the following template files:
`index.html` - The homepage, provides links and information about the other routes 
`dashboard.html` - The control panel, provides the user with the latest metrics and AI report, and the options to start/stop a simulation and to wipe the logs
`detailedreport.html` - Contains a longer and much more detailed report of system and database state
`ai_logs.html` - Provides a list of AI insights. Can be used to analyse historical trends

All these files inherit metadata, CSS and the nav-bar from `base.html` this is achieved using Jinja2

## Evaluation Metrics

* **Healthy State:** CPU < 80%, RAM < 80%, Slow Queries < 5.
* **Critical State:** Triggered when any single metric exceeds thresholds; visually represented by badges in the dashboard.

---

## Future Roadmap

While the current architecture meets its core monitoring objectives, I will provide a list of possible improvements and how I would achieve them

1. Add buttons for starting/closing the collector, and modify its parameters(such as interval, amount of samples). This will be achieved in a similar manner to the aforementioned simulation manager(Creating a collector manager that listens so START, STOP and MODIFY commands)
2. Add an "amount" parameter to the simulation field, so that the user may choose to simulate concurrent database queries, or a DDoS volumetric attack if they wish to see what the collector outputs(or if the AI catches it). This can be achieved by starting multiple worker threads. 
3. A section where the user can introduce manual reports. This one may require some modification on how I store data. I may choose to add a "user_insight" field to each object stored in ai_insights.json, or a whole new object dedicated for this.
