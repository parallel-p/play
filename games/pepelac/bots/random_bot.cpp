#include <cstdio>
#include <iostream>
#include <ctime>
#include <algorithm>

using namespace std;

const int MaxN = int(1e5) + 100;

int n, p, s, k;
int px[MaxN], py[MaxN], pb[MaxN];
int bx[MaxN], by[MaxN];
int dx[] = {0, 0, 0, 1, -1};
int dy[] = {0, 1, -1, 0, 0};
string turn[] = {"STAND", "RIGHT", "LEFT", "DOWN", "UP"};

inline bool check(int x, int y)
{
  return x >= 1 && x <= n && y >= 1 && y <= n;
}

int main()
{
  scanf("%d", &n);
  while (1)
  {
    scanf("%d%d%d", &p, &s, &k);
    for (int i = 0; i < p; ++i)
      scanf("%d%d%d", &px[i], &py[i], &pb[i]);
    for (int i = 0; i < s; ++i)
      scanf("%d%d", &bx[i], &by[i]);
    srand(time(NULL));
    while (1)
    {
      int index = rand() % 5;
      if (check(px[0] + dx[index], py[0] + dy[index]))
      {
        printf("%s\n", turn[index].c_str());
        break;
      }
    }
    fflush(stdout);
  }
  return 0;  
}
