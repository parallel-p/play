#include <stdio.h>
#include <algorithm>
#include <iostream>

using namespace std;

struct player
{
    int x, y, p;
};

struct bullet
{
    int x, y, dist[50], g, mn;
};

const int dx[4] = {1, 0, -1, 0};
const int dy[4] = {0, 1, 0, -1};

int n, p, b, k, x = 1, y = 1, bx, by, t;
int c[100][100];
bool used[100][100], made_move;
player players[50];
bullet bullets[100000];

bool comp_bullets(bullet a, bullet b)
{
    return a.g > b.g;
}

bool good_move(int x, int y)
{
    return (x >= 1 && x <= n && y >= 1 && y <= n && c[y][x] < k - 1 && !used[y][x]);
}

int sign(int x)
{
    if (x < 0)
        return -1;
    return (x > 0);
}

int main()
{
    scanf("%d", &n);
    for (int i = 1; i <= n * n; i++)
    {
        c[y][x] = -i;
        used[y][x] = true;
        if (x + dx[t] <= 0 || x + dx[t] > n ||
                y + dy[t] <= 0 || y + dy[t] > n ||
                used[y + dy[t]][x + dx[t]])
            t = (t + 1) % 4;
        if (i == n * n)
        {
            bx = x;
            by = y;
        }
        x += dx[t];
        y += dy[t];
    }
    while (true)
    {
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                used[i][j] = false;
        scanf("%d%d%d", &p, &b, &k);
        for (int i = 0; i < p; i++)
        {
            scanf("%d%d%d", &players[i].y, &players[i].x, &players[i].p);
            used[players[i].y][players[i].x] = true;
        }
        for (int i = 0; i < b; i++)
            scanf("%d%d", &bullets[i].y, &bullets[i].x);
        x = players[0].x;
        y = players[0].y;
        if (p == 1)
        {
            if (good_move(x + 1, y))
                printf("RIGHT\n");
            else
                if (good_move(x - 1, y))
                    printf("LEFT\n");
                else
                    if (good_move(x, y + 1))
                        printf("DOWN\n");
                    else
                        if (good_move(x, y - 1))
                            printf("UP\n");
                        else
                            printf("STAND\n");
            fflush(stdout);
            continue;
        }
        for (int i = 0; i < b; i++)
            for (int j = 0; j < p; j++)
                bullets[i].dist[j] = abs(bullets[i].x - players[j].x) + abs(bullets[i].y - players[j].y);
        for (int i = 0; i < b; i++)
        {
            int mn = (1 << 30);
            for (int j = 1; j < p; j++)
                if (bullets[i].dist[j] < mn)
                    mn = bullets[i].dist[j];
            bullets[i].g = mn - bullets[i].dist[0];
            bullets[i].mn = mn;
        }
        sort(bullets, bullets + b, comp_bullets);
        made_move = false;
        for (int i = 0; i < b && !made_move; i++)
        {
            if (bullets[i].g >= 0 && c[bullets[i].x][bullets[i].y] < t - bullets[i].dist[0])
            {
                if (c[y][x + sign(bullets[i].x - x)] < t - 1 && bullets[i].x - x != 0 && !used[y][x + sign(bullets[i].x - x)])
                {
                    if (bullets[i].x - x > 0)
                        printf("RIGHT\n");
                    else
                        printf("LEFT\n");
                    fflush(stdout);
                    made_move = true;
                    break;
                }
                if (c[y + sign(bullets[i].y - y)][x] < t - 1 && bullets[i].y - y != 0 && !used[y + sign(bullets[i].y - y)][x])
                {
                    if (bullets[i].y - y > 0)
                        printf("DOWN\n");
                    else
                        printf("UP\n");
                    fflush(stdout);
                    made_move = true;
                    break;
                }
            }
        }
        if (!made_move)
        {
            if (bx - x != 0 && !used[y][x + sign(bx - x)])
            {
                if (bx - x > 0)
                    printf("RIGHT\n");
                else
                    printf("LEFT\n");
                fflush(stdout);
                continue;
            }
            if (by - y != 0 && !used[y + sign(by - y)][x])
            {
                if (by - y > 0)
                    printf("DOWN\n");
                else
                    printf("UP\n");
                fflush(stdout);
                continue;
            }
            printf("STAND\n");
            fflush(stdout);
        }
    }
    return 0;
}
