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
int big = 100000000;

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

  t = k;
  if (t <= 0 && stupid){
    t -= p - 1;
  }

  for (s = 1; t <= 0 && s < 2 * n; s++){
    for (i = s; i <= n - s && t <= 0; i++){
      dan[i][s] = 2 * big;
      t++;
    }
    for (i = s; i <= n - s && t <= 0; i++){
      dan[s][i] = 2 * big;
      t++;
    }
    for (i = n - s + 1; i >= s + 1 && t <= 0; i--){
      dan[i][n - s + 1] = 2 * big;
      t++;
    }
    for (i = n - s + 1; i >= s + 1 && t <= 0; i--){
      dan[n - s + 1][i] = 2 * big;
      t++;
    }
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

  if (players[0].x < x && !f && dan[players[0].x + 1][players[0].y] < big)
    f = right();
  if (players[0].x > x && !f && dan[players[0].x - 1][players[0].y] < big)
    f = left();
  if (players[0].y < y && !f && dan[players[0].x][players[0].y + 1] < big)
    f = down();
  if (players[0].y > y && !f && dan[players[0].x][players[0].y - 1] < big)
    f = up();
  if (!f)
    stay();
}

void safe(){
  int x = players[0].x, y = players[0].y, gx = x, gy = y;
  if (dan[gx][gy] > dan[x - 1][y]){
    gx = x - 1;
    gy = y;
  }
  if (dan[gx][gy] > dan[x + 1][y]){
    gx = x + 1;
    gy = y;
  }
  if (dan[gx][gy] > dan[x][y - 1]){
    gx = x;
    gy = y - 1;
  }
  if (dan[gx][gy] > dan[x][y + 1]){
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

    if (p > 1)
      armageddon();

    //cout << "armageddoned" << endl;

    if (p < 2){
      stay();
      //fuck yeah
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
          dan[j][0] = big;
          dan[j][n + 1] = big;
          dan[0][i] = big;
          dan[n + 1][i] = big;
        }

        if (dan[bullets[i].x][bullets[i].y] == big || (dan[bullets[i].x - 1][bullets[i].y] == big && dan[bullets[i].x + 1][bullets[i].y] == big && dan[bullets[i].x][bullets[i].y - 1] == big && dan[bullets[i].x][bullets[i].y  +1] == big))
          bullets[i].c = -100500;


      }

      bb = bullets[0];
      for (i = 1; i < b; i++){
        if (bb.c < bullets[i].c)
          bb = bullets[i];
      }
      //cout << "going to" << " " << bb.x << " " << bb.y << endl;
      go(bb.x, bb.y);
    }
    else if (p == 2 && players[0].b >= players[1].b + b){
      go(n / 2 + 1, n / 2 + 1);
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
