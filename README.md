
# Flask API with AWS EC2 and RDS Deployment

This is a Flask API that connects to a PostgreSQL database hosted on AWS RDS and can be deployed on an EC2 instance.

## Prerequisites
- AWS account
- AWS CLI installed and configured on your local machine
- Python 3.7+ installed

## Setup

1. Clone the repository and navigate into the project directory.

```bash
git clone https://github.com/your-repo/flask-api
cd flask-api
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables for database connection. Create a `.env` file with the following format:

```bash
DB_HOST=<your-rds-endpoint>
DB_PORT=5432
DB_NAME=<your-database-name>
DB_USER=<your-username>
DB_PASSWORD=<your-password>
```

4. Create the `items` table in your PostgreSQL database:

```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
```

---

## Deploying to AWS

### Step 1: Set Up RDS

1. Go to the RDS section in the AWS Console and create a PostgreSQL instance.
2. In **Connectivity & Security**:
   - Enable **Public Access**.
   - Configure the **VPC security group** to allow inbound traffic on the PostgreSQL port (default is 5432) from your EC2 instance.
3. After the instance is created, note down the **endpoint** and **port**.

### Step 2: Set Up EC2

1. Go to the EC2 section in the AWS Console and launch a new instance:
   - Select an Amazon Linux or Ubuntu instance.
   - Choose an instance type (t2.micro is recommended for testing).
   - Configure the **security group** to allow inbound traffic on ports 22 (SSH) and 5000 (Flask app).

2. SSH into your EC2 instance using the key pair you specified when creating the instance:

```bash
ssh -i /path/to/key.pem ec2-user@your-ec2-public-ip
```

3. Update packages and install necessary software on EC2:

```bash
# Update the package lists
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip -y

# Install virtualenv (recommended)
pip3 install virtualenv
```

4. Clone your repository on EC2:

```bash
# Clone the repository
git clone https://github.com/your-repo/flask-api.git
cd flask-api

# Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate
```

5. Install the dependencies:

```bash
pip install -r requirements.txt
```

6. Configure your `.env` file on EC2 with the database credentials for RDS:

```bash
echo "DB_HOST=<your-rds-endpoint>" >> .env
echo "DB_PORT=5432" >> .env
echo "DB_NAME=<your-database-name>" >> .env
echo "DB_USER=<your-username>" >> .env
echo "DB_PASSWORD=<your-password>" >> .env
```

### Step 3: Run the Flask App

1. Start the Flask app:

```bash
# Set Flask to listen on all interfaces and port 5000
flask run --host=0.0.0.0 --port=5000
```

2. Test the app by going to your EC2 public IP and port 5000 in the browser or using `curl`:

```bash
curl http://<your-ec2-public-ip>:5000/health
```

---

## Configuring Flask as a Service (Optional)

To run Flask as a background service on EC2:

1. Create a systemd service file for the Flask app:

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

2. Add the following content to the file:

```ini
[Unit]
Description=Flask Application
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/flask-api
Environment="DB_HOST=<your-rds-endpoint>"
Environment="DB_PORT=5432"
Environment="DB_NAME=<your-database-name>"
Environment="DB_USER=<your-username>"
Environment="DB_PASSWORD=<your-password>"
ExecStart=/home/ec2-user/flask-api/venv/bin/python /home/ec2-user/flask-api/app.py

[Install]
WantedBy=multi-user.target
```

3. Reload the systemd daemon, start the service, and enable it to start on boot:

```bash
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
```

4. Verify the service is running:

```bash
sudo systemctl status flaskapp
```

---

## Testing the API

### Available Endpoints

- **GET /health**: Check the health of the API and database connection.
- **POST /items**: Create a new item.
- **GET /items/<item_id>**: Retrieve an item by ID.
- **PUT /items/<item_id>**: Update an item by ID.
- **DELETE /items/<item_id>**: Delete an item by ID.

```bash
# Example curl request
curl http://<your-ec2-public-ip>:5000/health
```

Your API is now deployed and connected to an RDS PostgreSQL database on AWS.
