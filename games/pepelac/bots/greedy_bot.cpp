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

bool debug = 0, stupid = 0;
int big = 10000000;

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
  if (players[0].x == 1){
    return 0;
  }
  else{
    players[0].x--;
    cout << "UP" << endl;

    debug || cout.flush();
    return 1;
  }
}

bool down(){
  if (players[0].x == n){
    return 0;
  }
  else{
    players[0].x++;
    cout << "DOWN" << endl;
    debug || cout.flush();
    return 1;
  }
}

bool left(){
  if (players[0].y == 1){
    return 0;
  }
  else{
    players[0].y--;
    cout << "LEFT" << endl;
    debug || cout.flush();
    return 1;
  }
}

bool right(){
  if (players[0].y == n){
    return 0;
  }
  else{
    players[0].y++;
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
    players.push_back(player(t1, t2, t3));
  }
  //players.push_back(player(t1, t2, t3));

  bullets.clear();
  for (i = 0; i < b; i++){
    cin >> t1 >> t2;
    bullets.push_back(bullet(t1, t2));
  }
  //bullets.push_back(bullet(t1, t2));
}

void armageddon(){
  int i, j, t, s;
  for (i = 1; i <= n; i++){
    for (j = 1; j <= n; j++){
      dan[i][j] = 0;
      isbul[i][j] = 0;
    }
  }

  for (i = 0; i < b; i++)
    isbul[bullets[i].x][bullets[i].y] = 1;

  for (i = 1; i < p; i++){

    dan[players[i].x][players[i].y] = big;
    if (players[i].b > players[0].b){
      dan[players[i].x][players[i].y - 1] = big;
      dan[players[i].x][players[i].y + 1] = big;
      dan[players[i].x - 1][players[i].y] = big;
      dan[players[i].x + 1][players[i].y] = big;
      dan[players[i].x + 2][players[i].y] = big;
      dan[players[i].x][players[i].y + 2] = big;
      if (players[i].x > 2)
        dan[players[i].x - 2][players[i].y] = big;
      if (players[i].y > 2)
        dan[players[i].x][players[i].y - 2] = big;
    }

    if (players[i].b > players[0].b){
      if (isbul[players[i].x][players[i].y - 1]){
        dan[players[i].x][players[i].y - 2] = big;
        dan[players[i].x - 1][players[i].y - 1] = big;
        dan[players[i].x + 1][players[i].y - 1] = big;
      }
      if (isbul[players[i].x][players[i].y + 1]){
        dan[players[i].x][players[i].y + 2] = big;
        dan[players[i].x - 1][players[i].y + 1] = big;
        dan[players[i].x + 1][players[i].y + 1] = big;
      }
      if (isbul[players[i].x - 1][players[i].y]){
        dan[players[i].x - 2][players[i].y] = big;
        dan[players[i].x - 1][players[i].y + 1] = big;
        dan[players[i].x - 1][players[i].y - 1] = big;
      }
      if (isbul[players[i].x + 1][players[i].y]){
        dan[players[i].x + 2][players[i].y] = big;
        dan[players[i].x + 1][players[i].y + 1] = big;
        dan[players[i].x + 1][players[i].y - 1] = big;
      }
    }

    int x = players[i].x, y = players[i].y;

    if (players[i].b == players[0].b){
      if (isbul[players[i].x][players[i].y - 1]){
        if (!isbul[x][y - 2])
          dan[players[i].x][players[i].y - 2] = big;
        if (!isbul[x - 1][y - 1])
          dan[players[i].x - 1][players[i].y - 1] = big;
        if (!isbul[x + 1][y - 1])
          dan[players[i].x + 1][players[i].y - 1] = big;
      }
      if (isbul[players[i].x][players[i].y + 1]){
        if (!isbul[x][y + 2])
          dan[players[i].x][players[i].y + 2] = big;
        if (!isbul[x - 1][y + 1])
          dan[players[i].x - 1][players[i].y + 1] = big;
        if (!isbul[x + 1][y + 1])
          dan[players[i].x + 1][players[i].y + 1] = big;
      }
      if (isbul[players[i].x - 1][players[i].y]){
        if (!isbul[x - 2][y])
          dan[players[i].x - 2][players[i].y] = big;
        if (!isbul[x - 1][y + 1])
          dan[players[i].x - 1][players[i].y + 1] = big;
        if (!isbul[x - 1][y - 1])
          dan[players[i].x - 1][players[i].y - 1] = big;
      }
      if (isbul[players[i].x + 1][players[i].y]){
        if (!isbul[x + 2][y])
          dan[players[i].x + 2][players[i].y] = big;
        if (!isbul[x + 1][y + 1])
          dan[players[i].x + 1][players[i].y + 1] = big;
        if (!isbul[x + 1][y - 1])
          dan[players[i].x + 1][players[i].y - 1] = big;
      }
    }

  }

  int v[4][2];
  v[0][0] = 0;
  v[0][1] = 1;
  v[1][0] = 1;
  v[1][1] = 0;
  v[2][0] = 0;
  v[2][1] = -1;
  v[3][0] = -1;
  v[3][1] = 0;

  int x = 1, y = 1, c;
  for (t = k; t <= 0; t++){
    dan[x][y] = 2 * big;
    x += v[c][0];
    y += v[c][1];
    if (x < 1 || y < 1 || x > n || y > n || dan[x][y] == 2 * big){
      x -= v[c][0];
      y -= v[c][1];
      c = (c + 1) % 4;
      x += v[c][0];
      y += v[c][1];
    }
  }

}

void go(int x, int y){
  bool f = 0;


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

  if (players[0].x < x && !f && dan[players[0].x + 1][players[0].y] < big)
    f = down();
  if (players[0].x > x && !f && dan[players[0].x - 1][players[0].y] < big)
    f = up();
  if (players[0].y < y && !f && dan[players[0].x][players[0].y + 1] < big)
    f = right();
  if (players[0].y > y && !f && dan[players[0].x][players[0].y - 1] < big)
    f = left();

  if (players[0].x < x && !f && dan[players[0].x + 1][players[0].y] < big)
    f = left() || right();
  if (players[0].x > x && !f && dan[players[0].x - 1][players[0].y] < big)
    f = left() || right();
  if (players[0].y < y && !f && dan[players[0].x][players[0].y + 1] < big)
    f = up() || down();
  if (players[0].y > y && !f && dan[players[0].x][players[0].y - 1] < big)
    f = up() || down();
  if (!f)
    stay();
}

void safe(){

  //stay();
  //return;

  int x = players[0].x, y = players[0].y, gx = x, gy = y;
  if (x > 1 && dan[gx][gy] > dan[x - 1][y]){
    gx = x - 1;
    gy = y;
  }
  if (x < n && dan[gx][gy] > dan[x + 1][y]){
    gx = x + 1;
    gy = y;
  }
  if (y > 1 && dan[gx][gy] > dan[x][y - 1]){
    gx = x;
    gy = y - 1;
  }
  if (y < n && dan[gx][gy] > dan[x][y + 1]){
    gx = x;
    gy = y + 1;
  }
  go(gx, gy);
}



int main(){
  //freopen("input.txt", "r", stdin);
  //freopen("output.txt", "w", stdout);



  int i, f, i1, j1;
  Bullet bb;
  cin >> n;//field size

  while (1){
    read();
    //cout << "read" << endl;


    armageddon();

    //cout << "armageddoned" << endl;

    if (p < 2){
      safe();
      //fuck yeah
    }
    else if (p == 2 && players[0].b >= players[1].b + b){
      go(n / 2 + 1, n / 2 + n % 2);
    }
    else if (b > 0){



      for (i = 0; i < b; i++){
        bullets[i].c = 2 * n - abs(bullets[i].x - players[0].x) - abs(bullets[i].y - players[0].y);
        if (players[0].b < players[1].b){
          bullets[i].c += abs(bullets[i].x - players[1].x) + abs(bullets[i].y - players[1].y);
        }
        else{
          bullets[i].c += 2 * n;
        }

        for (i1 = max(1, bullets[i].x - 3); i1 <= min(n, bullets[i].x + 3); i1++){
          for (j1 = max(1, bullets[i].y - 3); j1 <= min(n, bullets[i].y + 3); j1++){
            bullets[i].c += isbul[i1][j1] * n / 4;
          }
        }

        for (int j = 0; j <= n + 1; j++){
          dan[j][0] = 3 * big;
          dan[j][n + 1] = 3 * big;
          dan[0][i] = 3 * big;
          dan[n + 1][i] = 3 * big;
        }

        if (dan[bullets[i].x][bullets[i].y] >= big || (dan[bullets[i].x - 1][bullets[i].y] >= big && dan[bullets[i].x + 1][bullets[i].y] >= big && dan[bullets[i].x][bullets[i].y - 1] >= big && dan[bullets[i].x][bullets[i].y + 1] >= big))
          bullets[i].c = -100500;


      }

      bb = bullets[0];
      for (i = 1; i < b; i++){
        if (bb.c < bullets[i].c && dan[bullets[i].x][bullets[i].y] < big)
          bb = bullets[i];
      }
      //cout << "going to" << " " << bb.x << " " << bb.y << endl;
      if (dan[bb.x][bb.y] < big)
        go(bb.x, bb.y);
      else
        safe();

    }
    else{
      debug && (cout << "oh fuck" << endl);
      safe();
      //failed
    }

    //cout << "steped" << endl;

  }


  return 0;
}
