#include <cstdio>
#include <iostream>
#include <ctime>
#include <vector>
#include <algorithm>

#define fst first
#define snd second
#define mp make_pair
#define pb push_back

using namespace std;

const int INF = int(1e9);

typedef pair <int, int> pii;

const int MAX_N = 100;
const int MOVES[4][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
const int GO[5][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}, {0, 0}};
const string TURNS[] = {"RIGHT", "DOWN", "LEFT", "UP", "STAND"};

struct pt
{
  int x, y;              
  pt() {}
  pt(int a, int b) {x = a, y = b;}
  void read()
  {
    scanf("%d%d", &x, &y);
    --x, --y;
  }
};

int n, p, s, k;
pt players[MAX_N], bullets[MAX_N];
int bullets_count[MAX_N];
int table[MAX_N][MAX_N];
int direction;
pii last_exploded;

inline void make_move(int move)
{
  printf("%s\n", TURNS[move].c_str());
  fflush(stdout);
}

inline bool good_cell_to_explode(pii cell)
{
  return cell.fst >= 0 && cell.fst < n && cell.snd >= 0 && cell.snd < n && table[cell.fst][cell.snd] != -2;
}

inline bool good_cell(pii cell, int player)
{
  return good_cell_to_explode(cell) && (table[cell.fst][cell.snd] <= 0 || table[cell.fst][cell.snd] == player);
} 

inline int distance_between_cells(pii cell_from, pii cell_to)
{
  return abs(cell_from.fst - cell_to.fst) + abs(cell_from.snd - cell_to.snd);
}
 
inline void explode_cell()
{
  pii next_cell = mp(last_exploded.fst + MOVES[direction][0], last_exploded.snd + MOVES[direction][1]);
  if (!good_cell_to_explode(next_cell))
    direction = (direction + 1) % 4;
  last_exploded = mp(last_exploded.fst + MOVES[direction][0], last_exploded.snd + MOVES[direction][1]);
  table[last_exploded.fst][last_exploded.snd] = -2;
}

inline void one_player()
{
  pii finish = mp((n - 1) / 2 + (n - 1) % 2, (n - 1) / 2);
  
  int min_distance = INF;
  int best_turn = 0;
  for (int turn = 0; turn < 5; ++turn)
  {
    pii new_cell = mp(players[0].x + GO[turn][0], players[0].y + GO[turn][1]);
    if (good_cell(new_cell, 1) && min_distance > distance_between_cells(new_cell, finish))
      min_distance = distance_between_cells(new_cell, finish), best_turn = turn;
  }
  make_move(best_turn);
}

inline bool check(int x, int y)
{
  return x >= 0 && x < n && y >= 0 && y < n && table[x][y] != -2;
}

int main()
{
  scanf("%d", &n);
  bool is_initialized = 0;
  direction = 0;
  last_exploded = mp(0, -1);
  while (1)
  {
    for (int i = 0; i < MAX_N; ++i)
      for (int j = 0; j < MAX_N; ++j)
        if (table[i][j] != -2)
          table[i][j] = 0;
    scanf("%d%d%d", &p, &s, &k);
    
    if (!is_initialized && k < 0)
      for (int i = 0; i < -k; ++i)
        explode_cell();
    if (k <= 0)
      explode_cell();

    for (int i = 0; i < p; ++i)
    {
      players[i].read();
      scanf("%d", &bullets_count[i]);
      if (table[players[i].x][players[i].y] != -2)
        table[players[i].x][players[i].y] = i + 1;
    }
    for (int i = 0; i < s; ++i)
    {
      bullets[i].read();
      if (table[bullets[i].x][bullets[i].y] != -2)
        table[bullets[i].x][bullets[i].y] = -1;
    }

    if (table[players[0].x][players[0].y] == -2)
    {   
      srand(time(NULL));
      bool out = 0;
      for (int i = 0; i < 100; i++)
      {
        int index = rand() % 4;
        if (check(players[0].x + GO[index][0], players[0].y + GO[index][1]))
        {
          printf("%s\n", TURNS[index].c_str());
          out = 1;
          break;
        }
      }
      if (!out)
        puts("STAND");
      fflush(stdout);
      continue;
    }
    
    if (p == 1)
    {
      one_player();
      continue;
    }

    srand(time(NULL));
    while (1)
    {
      int index = rand() % 5;
      if (check(players[0].x + GO[index][0], players[0].y + GO[index][1]))
      {
        printf("%s\n", TURNS[index].c_str());
        break;
      }
    }
    fflush(stdout);
  }
  return 0;  
}
