#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>
#include <string>
#include <atomic>
#include <chrono>
#include <filesystem>
#include <sstream>
#include <thread>
#include <set>
using namespace std;
namespace fs = std::filesystem;
constexpr fs::perms all_permissions =
  fs::perms::owner_read | fs::perms::owner_write | fs::perms::owner_exec |
  fs::perms::group_read | fs::perms::group_write | fs::perms::group_exec |
  fs::perms::others_read | fs::perms::others_write | fs::perms::others_exec;



string template_file_names = "template.tbl";
string directory_path = "./";
set<string> names_of_files_to_protect{template_file_names};
void setAttr(const string& file_path) {
  if (fs::is_directory(file_path)) return;
    string command = "chmod a-rwx " + file_path + " && chattr +i " + file_path;
    //cout << "Command to execute: " << command << endl;  
    int result = system(command.c_str());
    if (result != 0) {
      cerr << "Error executing command: " << result << endl;
    }
}
void unsetAttr(const string& file_path) {
  if (fs::is_directory(file_path)) return;
  string command = "chattr -i " + file_path + " && chmod u+rw " + file_path;
  //cout << "Command to execute: " << command << endl;  
  int result = system(command.c_str());
  if (result != 0) {
    cerr << "Error executing command: " << result << endl;
  }
}

string hash_password(const string& password) {
  hash<string> hasher;
  size_t hash_value = hasher(password);  ostringstream oss;
  oss << hex << setw(16) << setfill('0') << hash_value;
  string long_hash = oss.str();
  return long_hash;
}

void enable_protection(const string& directory_path, const set<std::string>& protected_files_name){
  ifstream template_files(template_file_names);
  
  string line;
  while (getline(template_files, line)) {
    names_of_files_to_protect.insert(line);
  }
  for (const auto& file : fs::directory_iterator(directory_path)) {
    auto it = names_of_files_to_protect.find(file.path().filename());
    if (it != names_of_files_to_protect.end()) {
      setAttr(file.path());
    }
  }
}
void disableProtection(const string& directory_path, const set<string>& protected_files_name) {
  for (const auto& file : fs::directory_iterator(directory_path)) {
    auto it = names_of_files_to_protect.find(file.path().filename());
    if (it != names_of_files_to_protect.end()){
      unsetAttr(file.path());
    }
  }
}

void startMonitoring(const string& directory_path,const set<string>& protected_files_name,atomic<bool>& exit_thread) {
  while (!exit_thread) {
    for (const auto& file : fs::directory_iterator(directory_path)) {
      std::string file_name = file.path().filename();
      if (fs::is_directory(file_name)) continue;
      if (protected_files_name.find(file_name) != protected_files_name.end()) {
        fs::file_status status = fs::status(file.path());
        fs::perms permissions = status.permissions();
        if ((permissions & all_permissions) != fs::perms::none) {
          fs::remove_all(file.path());
        }
      }
    }
  this_thread::sleep_for(std::chrono::milliseconds(10));  
  } 
}



bool checkpass(string password){
  string has_pass = hash_password(password);
  string passwordHash;
  if (access(template_file_names.c_str(), F_OK) != -1) {
    ifstream templateStream(template_file_names);
    if (templateStream.is_open()) {
      getline(templateStream, passwordHash);
      templateStream.close();
    } 
    else {
      cerr << "Ошибка при открытии файла template.tbl" << endl;
      return 1;}
    } 
    else {
      cerr << "Файл template.tbl не существует." << endl;
      return 1;
    }
    if (has_pass != passwordHash)
    {
      return false;
    }

    return true;
}


void menu(){
  cout << "1. Включить защиту" << endl;
  cout << "2. Выключить защиту" << endl;
  cout << "3. Выход из программы" << endl << endl;
}



int main(){
  int choice = 1;
  atomic<bool> exit_thread(false);  
  thread monitor_thread;
  string us_pass;
  while(choice){
    menu();
    cin >> choice; 
    switch(choice){
    case 1:
      cout << "Введите пароль " << endl;
      cin.ignore();
      getline(cin, us_pass);
      if (checkpass(us_pass)){
          enable_protection(directory_path, names_of_files_to_protect);
            monitor_thread = thread([&]() {
            startMonitoring(directory_path, names_of_files_to_protect, exit_thread);
          });
      }
      else{
        cout << "Не верный пароль !!" << endl;
      }
      break;
    case 2:
      cout << "Введите пароль " << endl;
      cin.ignore();
      getline(cin, us_pass);
      if (checkpass(us_pass)){
          exit_thread = true; 
          monitor_thread.join();
          disableProtection(directory_path, names_of_files_to_protect);
      } 
      else{
        cout << "Не верный пароль !!" << endl;
      }
      break;
    case 3:
      return 0;
    }
  }
}
