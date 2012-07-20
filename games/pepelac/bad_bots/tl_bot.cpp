#include <stdio.h>
#include <vector>
#include <algorithm>
#include <stdlib.h>
#include <set>
#include <map>
#include <iostream>
#include <string>
#include <iomanip>


using namespace std;


int big = 100000000;
bool debug = 0, stupid = 0;

struct Player{
   int x, y, b;
};

Player player(int x, int y, int b){
  Player t;
  t.x = x;
  t.y = y;
  t.b = b;
  return t;
}

struct Bullet{
   int x, y, c;
};

Bullet bullet(int x, int y){
  Bullet t;
  t.x = x;
  t.y = y;
  t.c = 0;
  return t;
}


int n, p, k, b, dan[100][100];
bool isbul[100][100];
vector<Player> players;
vector<Bullet> bullets;


bool up(){
  if (players[0].y == 1){
    return 0;
  }
  else{
    players[0].y--;
    cout << "UP" << endl;

    debug || cout.flush();
    return 1;
  }
}

bool down(){
  if (players[0].y == n){
    return 0;
  }
  else{
    players[0].y++;
    cout << "DOWN" << endl;
    debug || cout.flush();
    return 1;
  }
}

bool left(){
  if (players[0].x == 1){
    return 0;
  }
  else{
    players[0].x--;
    cout << "LEFT" << endl;
    debug || cout.flush();
    return 1;
  }
}

bool right(){
  if (players[0].x == n){
    return 0;
  }
  else{
    players[0].x++;
    cout << "RIGHT" << endl;
    debug || cout.flush();
    return 1;
  }
}

bool stay(){
  cout << "STAND" << endl;
  debug || cout.flush();
  return 1;
}



void read(){
  int i, t1, t2, t3 ,j;
  cin >> p >> b >> k;//bullets, players, rounds before armagedonn

  players.clear();
  for (i = 0; i < p; i++){
    cin >> t1 >> t2 >> t3;
    players.push_back(player(t2, t1, t3));
  }

  bullets.clear();
  for (i = 0; i < b; i++){
    cin >> t1 >> t2;
    bullets.push_back(bullet(t2, t1));
  }
}


void go(int x, int y){
  bool f;
  debug && (cout << "going to" << y <<  " " << x << endl);

  if (debug){
    for (int i = 1; i <= n; i++){
      for (int j = 1; j <= n; j++){
        cout << dan[j][i] << " ";
      }
      cout << endl;
    }

    for (int i = 0; i < b; i++){
      cout << bullets[i].y << " " << bullets[i].x << "   " << bullets[i].c << endl;
    }
  }

  /*if (!f && isbul[x - 1][y] && dan[x - 1][y] < big){
    f = left();
  }
  if (!f && isbul[x + 1][y] && dan[x + 1][y] < big){
    f = right();
  }
  if (!f && isbul[x][y - 1] && dan[x][y - 1] < big){
    f = up();
  }
  if (!f && isbul[x][y + 1] && dan[x][y + 1] < big){
    f = down();
  }*/


  if (!f && x == players[0].x && y == players[0].y)
    f = stay();

  if (players[0].x < x && !f)
    f = right();
  if (players[0].x > x && !f)
    f = left();
  if (players[0].y < y && !f)
    f = down();
  if (players[0].y > y && !f)
    f = up();
  if (!f)
    stay();
}


int main(){
  //freopen("input.txt", "r", stdin);
  //freopen("outputtxt", "w", stdout);

  read();
  stay();
  read();
  while(1){
    //wait...
  }


  return 0;
}
