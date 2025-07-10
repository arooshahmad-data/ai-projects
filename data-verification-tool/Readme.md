# 🛠 Data Verification Tool  

## 📌 Overview  
This tool allows users to **verify image-text pairs** by loading images and their corresponding text files from a selected directory. The images and texts are matched based on filenames.  

### 📂 Folder Structure  
When selecting a folder, ensure it contains the following subfolders:  
- **`images/`** – Stores the image files (e.g., `image1.jpg`).  
- **`texts/`** – Stores the corresponding text files (e.g., `image1.txt`).  
- The tool will **automatically match** images with text files based on their names.  

## 🚀 Running the Tool  
### 🔧 Using Python Script  
Run the following script to start the tool:  
```bash
    python dataverificationtool.py
``` 

## 🖥️ Using the Windows Executable
For Windows users, an executable version is available:

```commandline
    dist/dataverificationtool.exe
```

## 🎛 Features & Controls  
The interface includes the following **buttons**:  

| **Button**    | **Function**                                   |
|--------------|-------------------------------------------------|
| **Previous**  | Loads the previous image.                      |
| **Next**      | Loads the next image.                          |
| **Correct**   | Marks an image as **correct**.                 |
| **Incorrect** | Marks an image as **incorrect**.               |
| **Edit Text** | Allows editing the associated text file.       |
| **Save Text** | Saves the **edited text** file.                |

This tool helps efficiently verify and manage **image-text datasets**! 🚀  
