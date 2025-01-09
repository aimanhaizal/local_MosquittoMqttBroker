# How to setup Mosquitto MQTT Broker using docker 
This guide is a mixture of a guide by sukesh-ak ['setup-mosquitto-with-docker'](https://github.com/sukesh-ak/setup-mosquitto-with-docker/blob/main/README.md) as well as chat-GPT instructions.
These instructions is an extremely simple guide to setup an mqtt broker with anonymous connections ```(allow_anonymous false)``` as well as a simple subscribing and publishing.
___
Here's a streamlined guide for setting up a Mosquitto MQTT broker in Docker without authentication or advanced configurations:

---
### 1. Prerequisites

Ensure Docker is installed. For Debian-based systems, you can install Docker with:

```bash
sudo apt update
sudo apt install docker.io
```

Check Docker installation with:

```bash
docker --version
```

---

### 2. Create a Folder for Mosquitto Configuration

```bash
mkdir mosquitto
cd mosquitto

# Create subfolders for config and data
mkdir config data log
```

---

### 3. Create a Minimal Mosquitto Configuration File

```bash
nano config/mosquitto.conf
```

Add the following content to allow anonymous connections and define the listener port:

```
allow_anonymous true
listener 1883
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
```

---

### 4. Run the Mosquitto MQTT Broker with Docker

Run the Mosquitto container using the official image:

```bash
docker run -d \
  --name mosquitto \
  -p 1883:1883 \
  -v "$(pwd)/config:/mosquitto/config" \
  -v "$(pwd)/data:/mosquitto/data" \
  -v "$(pwd)/log:/mosquitto/log" \
  eclipse-mosquitto
```
If port ```1883``` is being used by another container, then connect mosquitto broker to another port ```1884```:

```bash
docker run -d \
  --name mosquitto \
  -p 1884:1883 \
  -v "$(pwd)/config:/mosquitto/config" \
  -v "$(pwd)/data:/mosquitto/data" \
  -v "$(pwd)/log:/mosquitto/log" \
  eclipse-mosquitto
```
---

### 5. Verify the Container is Running

Check if the container is up:

```bash
docker ps
```

Logs can be checked with:

```bash
docker logs mosquitto
```

---

### 6. Test the MQTT Broker

Install the Mosquitto client tools:

```bash
sudo apt install mosquitto-clients
```

**Subscriber:** Start a subscriber to listen to a topic:

```bash
mosquitto_sub -h localhost -p 1884 -t "test/topic"
```

**Publisher:** Publish a message to the topic:

```bash
mosquitto_pub -h localhost -p 1884 -t "test/topic" -m "Hello Mosquitto"
```

---

### 7. Additionals

If you are unable to save the ```mosquitto.conf``` file because of ```(NoPermissions (FileSystemError): Error: EACCES: permission denied, open '/home/work/mqtt5/config/mosquitto.conf')```, then you need to change the permissions to allow for writing the file.

  **Step 1: Check File Permissions**
   Make sure that you have the necessary permissions to write to the file. You can check and modify the permissions using the following steps.
   - Open a terminal on your remote server (or local machine if applicable).
   - Navigate to the directory where the `mosquitto.conf` file is located:
     ```bash
     cd /home/work/mqtt5/config/
     ```
   - Check the current file permissions by running:
     ```bash
     ls -l mosquitto.conf
     ```
     This will show the permissions, owner, and group associated with the file. For example:
     ```
     -rw-r--r-- 1 root root 1234 Jan 9 12:34 mosquitto.conf
     ```

     The output shows `rw-r--r--`, which means that the owner can read and write the file, but others can only read it. If you are not the file's owner, you may not have write permissions.

   **Step 2: Change file permissions**
   - Change the file's permissions to allow you to write to it.
   - To make the file writable for the owner, run:
     ```bash
     chmod u+w mosquitto.conf
     ```

   **Step 3: Change file ownership**
   If the file is owned by `root` or another user, you can change the ownership using the `chown` command:
   ```bash
   sudo chown yourusername:yourgroup mosquitto.conf
   ```

   Replace `yourusername` with your actual username and `yourgroup` with your group (usually the same as your username).
   Determine your username with the commands below:
   ```bash
whoami 
  id 
  sudo chown yourusername:yourgroup mosquitto.conf 
   ```   
