#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <vector>
#include <algorithm>

using namespace std;

const int inf = (1 << 30);

class Point{
public:
    int x, y;
    friend Point operator+(Point A, Point B){return Point(A.x + B.x, A.y + B.y);}
    friend Point operator-(Point A, Point B){return Point(A.x - B.x, A.y - B.y);}
    friend bool operator==(Point A, Point B){return A.x == B.x && A.y == B.y;}
    friend int dist(Point A, Point B){return abs(A.x - B.x) + abs(A.y - B.y);}

    Point(){}
    Point(int _x, int _y):x(_x), y(_y){}
};

class Player{
public:
    Point pos;
    int pc;
};

class Field{
private:
    int t[52][52];
public:
    int n;
    inline int& operator()(int x, int y){
        return t[x][y];
    }
    inline int& operator()(Point A){
        return t[A.x][A.y];
    }
    Field(){};
    Field(int N){
        n = N;
        memset(t, 0, sizeof t);
        for (int i = 0; i < N + 2; i++)
            t[i][0] = t[i][N + 1] = t[0][i] = t[N + 1][i] = -1;
    }
};

int N, P, B, T;
const Point LEFT(0, -1), RIGHT(0, +1), UP(-1, 0), DOWN(+1, 0), STAND(0, 0);
const Point ad[4] = {RIGHT, DOWN, LEFT, UP};
int armdir = 0;
Point armpos(1, 0), fc;

Player players[12000];
Point patrons[12000];

char *dirtostr(Point A){
    if (A == LEFT)
        return "LEFT";
    else if (A == RIGHT)
        return "RIGHT";
    else if (A == UP)
        return "UP";
    else if (A == DOWN)
        return "DOWN";
    else if (A == STAND)
        return "STAND";
}

void view_field(Field &field){
   fprintf(stderr, "View field:\n");
    for (int i = 1; i <= field.n; i++){
        for (int j = 1; j <= field.n; j++)
            fprintf(stderr, "% .1d ", field(i, j));
        fprintf(stderr, "\n");
    }
}

Point for_comp_points_by_dist_to_me;
bool comp_points_by_dist_to_me(Point A, Point B){
    return dist(for_comp_points_by_dist_to_me, A) <
           dist(for_comp_points_by_dist_to_me, B);
}

int fitness1(Field &field, int P, Player *players, int B, Point *patrons, Point D){
    Point &I = players[0].pos;
    I = I + D;
    int fitness = 0;
    int min_dist_to_patron = inf;
    int min_dist_to_player = inf;
    vector <Point> bpl, gpl;
    if (field(I) == -1 || armpos == I){
        fitness = -inf;
        goto END_of_fitness;
    }
    for (int i = 1; i < P; i++)
        if (I == players[i].pos){
            fitness = -inf;
            goto END_of_fitness;
        }

    for (int i = 1; i < P; i++)
        if (players[i].pc > players[0].pc)
            bpl.push_back(players[i].pos);
        else
            gpl.push_back(players[i].pos);
    for_comp_points_by_dist_to_me = I;
    sort(bpl.begin(), bpl.end(), comp_points_by_dist_to_me);
    sort(gpl.begin(), gpl.end(), comp_points_by_dist_to_me);
    sort(patrons, patrons + B, comp_points_by_dist_to_me);
    for (int i = 0; i < B && i < 5; i++)
        fitness -= 2 * dist(patrons[i], I);
    fitness -= dist(patrons[0], I) * 3;
    for (int i = 0; i < gpl.size() && i < 5; i++)
        fitness += dist(gpl[i], I) / 2;
    for (int i = 0; i < bpl.size() && i < 5; i++)
        fitness += dist(bpl[i], I);

    END_of_fitness:
    I = I - D;
    return fitness;
}


Point center1(Field &field, int P, Player *players, int B, Point *patrons){
    int best = -inf - 1, fit;
    Point bd;
    if ((fit = fitness1(field, P, players, B, patrons, STAND)) > best)
        best = fit, bd = STAND;
    if ((fit = fitness1(field, P, players, B, patrons, LEFT)) > best)
        best = fit, bd = LEFT;
    if ((fit = fitness1(field, P, players, B, patrons, RIGHT)) > best)
        best = fit, bd = RIGHT;
    if ((fit = fitness1(field, P, players, B, patrons, UP)) > best)
        best = fit, bd = UP;
    if ((fit = fitness1(field, P, players, B, patrons, DOWN)) > best)
        best = fit, bd = DOWN;
    return bd;
}


int fitness2(Field &field, int P, Player *players, int B, Point *patrons, Point D){
    Point &I = players[0].pos;
    I = I + D;
    int fitness = 0;
    int mindist = 10000, min2dist = 10000;
    if (field(I) == -1 || armpos == I || I == players[1].pos){
        fitness = -inf;
        goto END_of_fitness;
    }
    if (P == 1)
        goto END_of_fitness;
    if (P == 1 || players[0].pc >= players[1].pc + B){
        fitness = -dist(I, fc);
        goto END_of_fitness;
    }
    for (int i = 0; i < B; i++){
        if (dist(I, patrons[i]) < dist(players[1].pos, patrons[i]))
            mindist = min(mindist, dist(I, patrons[i])), min2dist = min(min2dist, dist(players[1].pos, patrons[i]));
    }
    fitness = -(mindist * 2 + min2dist);
    if (mindist == 0)
        players[0].pc++;
    if (players[0].pc < players[1].pc && dist(I, players[1].pos) < 3)
        fitness = -inf / 2;
    if (players[0].pc > players[1].pc && dist(I, players[1].pos) < 2)
        fitness = inf / 2;
    END_of_fitness:
    I = I - D;
    return fitness;
}


Point center2(Field &field, int P, Player *players, int B, Point *patrons){
    int best = -inf - 1, fit;
    Point bd;
    if ((fit = fitness2(field, P, players, B, patrons, STAND)) > best)
        best = fit, bd = STAND;
    if ((fit = fitness2(field, P, players, B, patrons, LEFT)) > best)
        best = fit, bd = LEFT;
    if ((fit = fitness2(field, P, players, B, patrons, RIGHT)) > best)
        best = fit, bd = RIGHT;
    if ((fit = fitness2(field, P, players, B, patrons, UP)) > best)
        best = fit, bd = UP;
    if ((fit = fitness2(field, P, players, B, patrons, DOWN)) > best)
        best = fit, bd = DOWN;
    return bd;
}


int main()
{
    //char str[100];
    //while (gets(str))
    //    cerr << str << endl;
    //return 0;
    scanf("%d", &N);
    Field field(N);
    fc = Point((N + 2) / 2, (N + 1) / 2);
    int t = 1;
    bool fl = 1;
    Point CC;
    while (true){
        scanf("%d%d%d", &P, &B, &T);
        while (t >= T){
            field(armpos) = -1;
            if (field(armpos + ad[armdir]) == -1)
                armdir = (armdir + 1) & 3;
            armpos = armpos + ad[armdir];
            t--;
            if (field(armpos) == -1){
                break;
            }
        }
        for (int i = 0; i < P; i++)
            scanf("%d%d%d", &players[i].pos.x, &players[i].pos.y, &players[i].pc);//, players[i].pos.x++, players[i].pos.y++;
        for (int i = 0; i < B; i++)
            scanf("%d%d", &patrons[i].x, &patrons[i].y);//, patrons[i].x++, patrons[i].y++;
        if (fl)
            fl = 0, CC = players[0].pos;
        /*cerr << "SP:" << CC.x << " " << CC.y << endl;
        Point &I = players[0].pos;
        int tm = field(I);
        field(I) = 1;
        view_field(field);
        field(I) = tm;*/
        if (P > 2)
            printf("%s\n", dirtostr(center1(field, P, players, B, patrons)));
        else
            printf("%s\n", dirtostr(center2(field, P, players, B, patrons)));
        fflush(stdout);
    }
    return 0;
}
