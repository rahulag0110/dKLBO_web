# Web App Setup and Running Instructions

## Section 1: First Time Installation

### 1. Install Docker

- **Download Docker Desktop:**
  - Visit the [Docker Desktop download page](https://www.docker.com/products/docker-desktop).
  - Download the installer for macOS.
- **Install Docker:**
  - Open the downloaded `.dmg` file and drag the Docker icon to your Applications folder.
  - Launch Docker from the Applications folder.
  - Follow the on-screen instructions to complete the installation.
  - Verify the installation by opening a terminal and running:
    ```bash
    docker --version
    ```

### 2. Configure Docker

- **Open Docker Settings:**
  - Click on the Docker icon in the menu bar and select **Preferences**.
- **Adjust Memory Allocation:**
  - Navigate to the **Resources** tab.
  - Increase the **Memory** allocation to **14 GB**.
  - Click **Apply & Restart** to save the changes and restart Docker.

### 3. Download and Prepare the Web App

- **Download the ZIP File:**
  - Obtain the ZIP file containing the repository from the provided link or source.
  - Save the ZIP file to your desired location.
- **Extract the ZIP File:**
  - Double-click the ZIP file to extract its contents.
  - Move the extracted folder to a convenient location on your Mac.

### 4. Build and Run the Application

- **Open Terminal:**
  - Launch the Terminal application from your Applications > Utilities folder.
- **Navigate to the Extracted Folder:**
  - Use the `cd` command to change the directory to the location of the extracted folder. For example:
    ```bash
    cd /path/to/extracted/folder
    ```
  - Replace `/path/to/extracted/folder` with the actual path to your extracted folder.
- **Build and Start the Application:**
  - Run the following command in the terminal:
    ```bash
    docker-compose up --build
    ```
  - The initial build process may take **15-30 minutes**. Docker will download and configure all necessary dependencies during this time.

### 5. Access the Web Application

- **Open Google Chrome:**
  - Make sure Google Chrome is installed. Download it from [here](https://www.google.com/chrome/) if needed.
- **Navigate to the Web Application:**
  - In Chrome, type `localhost:8080` in the address bar and press **Enter**.
  - The web application's interface should now be visible.

---

## Section 2: Running After Installation

### 1. Start Docker

- **Launch Docker:**
  - Open Docker from your Applications folder or ensure it’s running from the menu bar.

### 2. Run the Application

- **Open Terminal:**
  - Launch the Terminal application from your Applications > Utilities folder.
- **Navigate to the Project Folder:**
  - Use the `cd` command to change the directory to the location of the project folder. For example:
    ```bash
    cd /path/to/extracted/folder
    ```
  - Replace `/path/to/extracted/folder` with the actual path to your project folder.
- **Start the Application:**
  - Run the following command to start the application:
    ```bash
    docker-compose up
    ```
  - This time, the startup should be quick, taking less than **10 seconds**.

### 3. Access the Web Application

- **Open Google Chrome:**
  - Ensure Google Chrome is installed and open.
- **Navigate to the Web Application:**
  - In Chrome, type `localhost:8080` in the address bar and press **Enter**.
  - You should see the web application’s interface.

---

## Troubleshooting Tips

- **Docker Memory Issues:**
  - If Docker has performance issues, confirm the memory allocation is still set to 14 GB.
- **Port Conflicts:**
  - If `localhost:8080` doesn’t work, check for port conflicts or update the `docker-compose.yml` to use a different port.
- **Permission Issues:**
  - Ensure you have the necessary permissions to run Docker commands. You might need to use `sudo` for certain commands, especially if prompted for elevated privileges.

By following these instructions, you should be able to both set up the web app for the first time and run it subsequently with ease. For any issues or additional help, refer to the application's documentation or reach out to the support team.
