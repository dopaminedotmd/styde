#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::fs;
use std::process::Command;

#[tauri::command]
fn read_file(path: String) -> Result<String, String> {
    fs::read_to_string(&path).map_err(|e| format!("Failed to read {}: {}", path, e))
}

#[tauri::command]
fn write_file(path: String, content: String) -> Result<(), String> {
    let allowed = path.starts_with("D:\\")
        || path.starts_with(&std::env::var("USERPROFILE").unwrap_or_default());
    if !allowed {
        return Err("Path not allowed. Write access limited to D:\\ and user home.".into());
    }
    fs::write(&path, content).map_err(|e| format!("Failed to write {}: {}", path, e))
}

#[tauri::command]
fn search_files(pattern: String, path: String) -> Result<String, String> {
    let output = Command::new("rg")
        .args(["--no-heading", "-n", &pattern, &path])
        .output()
        .map_err(|e| format!("Search failed: {}", e))?;
    String::from_utf8(output.stdout).map_err(|e| format!("Invalid UTF-8: {}", e))
}

#[tauri::command]
fn hermes_command(args: Vec<String>) -> Result<String, String> {
    let output = Command::new("hermes")
        .args(&args)
        .output()
        .map_err(|e| format!("Hermes command failed: {}", e))?;
    String::from_utf8(output.stdout).map_err(|e| format!("Invalid UTF-8: {}", e))
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            read_file,
            write_file,
            search_files,
            hermes_command,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
