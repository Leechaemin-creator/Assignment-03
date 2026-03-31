#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>

using namespace std;

void wait(int milliseconds) {
    this_thread::sleep_for(chrono::milliseconds(milliseconds));
}

class CafeQueue {
private:
    vector<string> items;
    const int MAX_SIZE = 10;
    string last_action = "Queue 초기화 완료";

public:
    void display() {
        system("cls");
        cout << "---------------------------------------------------" << endl;
        cout << "                 [ 카페 무솔트 ]                   " << endl;
        cout << "---------------------------------------------------" << endl;
        cout << "  명령어: " << last_action << endl;
        cout << "  현재 큐 크기: " << items.size() << " / " << MAX_SIZE << endl;
        cout << "---------------------------------------------------" << endl;

        for (int i = MAX_SIZE - 1; i >= 0; i--) {
            if (i < (int)items.size()) {
                printf("                | %-20s |\n", items[i].c_str());
            }
            else {
                cout << "                |                      |" << endl;
            }
            cout << "                ------------------------" << endl;
        }

        if (!items.empty()) {
            cout << "                ^ [Front: " << items.front() << "]" << endl;
        }
        cout << "---------------------------------------------------" << endl;
        wait(2000); 
    }

    void enqueue(string item) {
        if (items.size() < MAX_SIZE) {
            items.push_back(item);
            last_action = "enqueue(\"" + item + "\")";
            display();
        }
        else {
            last_action = "Error: Queue Full! (넘침 방지)";
            display();
        }
    }

    void dequeue() {
        if (!items.empty()) {
            string removed = items.front();
            items.erase(items.begin());
            last_action = "dequeue() -> [" + removed + "] 완료";
            display();
        }
    }

    void front() {
        if (!items.empty()) {
            last_action = "front() -> 현재 가장 앞: " + items.front();
            display();
        }
    }

    void isEmpty() {
        string result = items.empty() ? "True" : "False";
        last_action = "isEmpty() -> " + result;
        display();
    }

    void clear() {
        items.clear();
        last_action = "clear() -> 모든 데이터 삭제 완료";
        display();
    }
};

int main() {
    CafeQueue myCafe;

    myCafe.display();

    string group1[] = {
        "말차라떼(제로슈가)", "초코스콘(제로슈가)", "바스크치즈케이크",
        "cafe latte", "lemon tea", "camomile tea",
        "매실티", "플레인 휘낭시에", "레몬에이드"
    };
    for (string menu : group1) myCafe.enqueue(menu);

    myCafe.front();
    myCafe.isEmpty();

    for (int i = 0; i < 8; i++) myCafe.dequeue();

    string group2[] = {
        "얼그레이라떼", "캐모마일티", "모히또에이드",
        "카푸치노", "초코스콘", "자몽티",
        "바닐라라떼", "말차라떼", "초코 휘낭시에"
    };
    for (string menu : group2) myCafe.enqueue(menu);

    for (int i = 0; i < 6; i++) myCafe.dequeue();

    string group3[] = {
        "아메리카노", "카페모카", "바스크치즈케이크",
        "카페라떼", "카푸치노", "말차라떼"
    };
    for (string menu : group3) myCafe.enqueue(menu);

    myCafe.front();

    myCafe.clear();

    myCafe.isEmpty();

    return 0;
}