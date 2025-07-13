# LPL-Demo

A demonstration project showcasing integrations between JIRA, MySQL, Docker, and Model Context Protocol (MCP).

## Project Structure

```
LPL-Demo/
├── docker-compose.yaml        # Multi-service Docker setup (JIRA, MySQL, Postgres)
├── requirements.txt           # Python dependencies
├── package.json               # Node.js dependencies
├── env.example                # Example environment variables
├── README.md                  # This file
└── ...                        # Other project files
```

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.11)
- Docker
- Access to a JIRA instance (local or cloud)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vsusheel/LPL-Demo.git
   cd LPL-Demo
   ```

2. Install dependencies:
   ```bash
   npm install
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

### Running with Docker Compose

Start JIRA, MySQL, and Postgres services:
```bash
docker-compose up -d
```

### JIRA & MySQL Integration Workflow

- **Query JIRA ticket status using MCP**
- **Sync ticket data to MySQL**
- **Update or query tickets from MySQL**

#### Example: Sync JIRA Ticket to MySQL

1. Query JIRA ticket status (using MCP or API)
2. Insert or update the ticket in MySQL:
   ```sql
   INSERT INTO jira_table (issue_key, summary, description, priority, status, assignee, reporter, created, updated)
   VALUES ('DEMO-1', 'Demo Ticket', 'Created via UI', 'Medium', 'In Progress', 'Unassigned', 'user@email.com', '2025-07-13 23:01:05', '2025-07-13 23:04:31')
   ON DUPLICATE KEY UPDATE summary=VALUES(summary), description=VALUES(description), priority=VALUES(priority), status=VALUES(status), assignee=VALUES(assignee), reporter=VALUES(reporter), created=VALUES(created), updated=VALUES(updated);
   ```

#### Query Tickets from MySQL
```bash
docker run -it --rm mysql:8.0 mysql -h<mysql_host> -P3306 -u<user> -p<password> mydb -e "SELECT * FROM jira_table;"
```

## Features

- [x] JIRA ticket status query via MCP
- [x] Sync JIRA tickets to MySQL
- [x] Docker Compose for multi-service orchestration
- [ ] Automated ticket sync scripts
- [ ] Web dashboard (coming soon)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Project Link: [https://github.com/vsusheel/LPL-Demo](https://github.com/vsusheel/LPL-Demo) 

## Testing & CI/CD

### Running Tests Locally

- **Node.js tests:**
  ```bash
  npm test
  ```
  (Runs Jest if JS tests exist, otherwise runs Python tests)

- **Python tests:**
  ```bash
  pytest
  ```

### CI/CD Process

- On every push or pull request, GitHub Actions will:
  1. Set up Node.js and Python environments
  2. Install dependencies
  3. Run `npm test` (which will run both JS and Python tests if present)
  4. Report test results in the PR/build logs

You can add your test files in the appropriate locations (e.g., `tests/` for Python, `src/__tests__/` for JS). 