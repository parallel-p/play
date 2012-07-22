#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <vector>
#include <algorithm>

#define ll(i)  ((long long)(i))
#define lf(i)  ((double)(i))

using namespace std;

typedef long long lld;
const lld inf = (1ll << 60);


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
    int trash;
public:
    int n;
    inline int& operator()(int x, int y){
        if (x < 1 || x > n || y < 1 || y > n)
            return trash = -1;
        return t[x][y];
    }
    inline int& operator()(Point A){
        if (A.x < 1 || A.x > n || A.y < 1 || A.y > n)
            return trash = -1;
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
int armdir;
Point armpos, fc;

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

inline lld sqr(lld a){return a * a;}

Point dist_fI_q[2501];
Field gdfI(Field &field, int P, Player *players){
    Field d(field.n);
    int maxd = field.n * field.n + 1;
    for (int i = 1; i <= field.n; i++)
        for (int j = 1; j <= field.n; j++)
            d(i, j) = maxd;
    for (int i = 1; i < P; i++){
        d(players[i].pos) = maxd - 1;
        if (players[i].pc > players[0].pc)
            for (int dx = -2; dx < 3; dx++)
                for (int dy = -2; dy < 3; dy++)
                    if(abs(dx) + abs(dy) < 3)
                        d(players[i].pos.x + dx, players[i].pos.y + dy) = maxd - 1;
    }
    int l = 1, r = 0;
    dist_fI_q[++r] = players[0].pos;
    d(players[0].pos) = 0;
    Point s;
    while (l <= r){
        s = dist_fI_q[l++];
        if (d(s + UP) == maxd)
            d(s + UP) = d(s) + 1,
            dist_fI_q[++r] = s + UP;
        if (d(s + DOWN) == maxd)
            d(s + DOWN) = d(s) + 1,
            dist_fI_q[++r] = s + DOWN;
        if (d(s + LEFT) == maxd)
            d(s + LEFT) = d(s) + 1,
            dist_fI_q[++r] = s + LEFT;
        if (d(s + RIGHT) == maxd)
            d(s + RIGHT) = d(s) + 1,
            dist_fI_q[++r] = s + RIGHT;
    }
    return d;
}


const lld s_fit = 1000000000ll;
lld fitness1(Field &field, int P, Player *players, int B, int b, Point *patrons, Point D){
    Point &I = players[0].pos;
    I = I + D;
    Field dist_fI = gdfI(field, P, players);
    long long fitness = 0;
    long long mindist = 10000, min2dist = 10000, sumpt = 0;
    if (field(I) == -1 || armpos == I){
        fitness = -inf;
        goto END_of_fitness;
    }
    for (int i = 1; i < P; i++){
        if (I == players[i].pos){
            fitness = -inf - 1;
            goto END_of_fitness;
        }
        sumpt += players[i].pc;
    }

    if (P == 1){
        fitness = -dist(I, fc);
        goto END_of_fitness;
    }
    for (int i = 0; i < b; i++){
        mindist = min(mindist, ll(dist(I, patrons[i])));
    }
    for (int i = 0; i < b; i++){
        bool nearest_for_me = true;
        for (int pl = 1; pl < P; pl++)
            if (dist(I, patrons[i]) >= dist(patrons[i], players[pl].pos)){
                nearest_for_me = false;
                break;
            }
        if (nearest_for_me)
            min2dist = min(min2dist, ll(dist(I, patrons[i])));
    }
    if (mindist != 0 && lf(mindist) / lf(min2dist) > 0.7)
        mindist = min2dist;
    if (mindist == 0)
        players[0].pc++;
    for (int i = 1; i < P; i++)
        if (players[0].pc < players[i].pc && dist(I, players[i].pos) < 3){
            fitness = -inf / 2;
            goto END_of_fitness;
        }
    for (int pl = 1; pl < P; pl++)
        if (players[0].pc <= players[pl].pc && dist(players[0].pos, players[pl].pos) == 2)
            for (int i = 0; i < b; i++)
                if (dist(players[0].pos, patrons[i]) == 1 &&
                    dist(players[pl].pos, patrons[i]) == 1){
                        fitness = -inf / 2;
                        goto END_of_fitness;
                    }
    if (P == 1 || players[0].pc >= sumpt + B){
        fitness = -dist(I, fc);
        goto END_of_fitness;
    }
    if (mindist == 0ll)
        fitness = s_fit * 2;
    else
        fitness = s_fit / sqr(mindist);
    for (int i = 0; i < b; i++){
        if (dist(patrons[i], I) == 0ll)
            continue;
        bool nearest_for_me = true;
        for (int pl = 1; pl < P; pl++)
            if (dist(I, patrons[i]) >= dist(patrons[i], players[pl].pos)){
                nearest_for_me = false;
                break;
            }
        if (nearest_for_me)
            fitness += s_fit / 7ll / dist_fI(patrons[i]);
        else
            fitness += s_fit / 49ll - dist_fI(patrons[i]);
    }


    END_of_fitness:
    I = I - D;
    return fitness;
}


Point center1(Field &field, int P, Player *players, int B, int b, Point *patrons){
    lld best = -inf - 2, fit;
    Point bd;
    if ((fit = fitness1(field, P, players, B, b, patrons, STAND)) > best)
        best = fit, bd = STAND;
    if ((fit = fitness1(field, P, players, B, b, patrons, LEFT)) > best)
        best = fit, bd = LEFT;
    if ((fit = fitness1(field, P, players, B, b, patrons, RIGHT)) > best)
        best = fit, bd = RIGHT;
    if ((fit = fitness1(field, P, players, B, b, patrons, UP)) > best)
        best = fit, bd = UP;
    if ((fit = fitness1(field, P, players, B, b, patrons, DOWN)) > best)
        best = fit, bd = DOWN;
    return bd;
}


lld fitness2(Field &field, int P, Player *players, int B, int b, Point *patrons, Point D){
    Point &I = players[0].pos;
    I = I + D;
    Field dist_fI = gdfI(field, P, players);
    long long fitness = 0;
    long long mindist = 10000, min2dist = 10000;
    if (field(I) == -1 || armpos == I || (I == players[1].pos && P == 2)){
        fitness = -inf - 1;
        goto END_of_fitness;
    }
    if (P == 1){
        fitness = -dist(I, fc);
        goto END_of_fitness;
    }
    for (int i = 0; i < b; i++)
        mindist = min(mindist, ll(dist_fI(patrons[i])));

    for (int i = 0; i < b; i++)
        if (dist_fI(patrons[i]) < dist(patrons[i], players[1].pos))
            min2dist = min(min2dist, ll(dist_fI(patrons[i])));
    if (mindist != 0 && lf(mindist) / lf(min2dist) > 0.7)
        mindist = min2dist;
    if (mindist == 0)
        players[0].pc++;
    if (players[0].pc < players[1].pc && dist(I, players[1].pos) < 3){
        fitness = -inf / 2;
        goto END_of_fitness;
    }
    if (players[0].pc > players[1].pc && dist(I, players[1].pos) < 2){
        fitness = inf / 2;
        goto END_of_fitness;
    }
    if (players[0].pc <= players[1].pc && dist(players[0].pos, players[1].pos) == 2)
        for (int i = 0; i < b; i++)
            if (dist(players[0].pos, patrons[i]) == 1 &&
                dist(players[1].pos, patrons[i]) == 1){
                    fitness = -inf / 2;
                    goto END_of_fitness;
                }
    if (players[0].pc >= players[1].pc + B){
        fitness = -dist(I, fc);
        goto END_of_fitness;
    }
    if (mindist == 0ll)
        fitness = s_fit * 2;
    else
        fitness = s_fit / sqr(mindist);
    for (int i = 0; i < b; i++){
        if (dist(patrons[i], I) == 0ll)
            continue;
        if (dist_fI(patrons[i]) < dist(patrons[i], players[1].pos))
            fitness += s_fit / 7ll / dist_fI(patrons[i]);
        else
            fitness += s_fit / 49ll - dist_fI(patrons[i]);
    }


    END_of_fitness:
    I = I - D;
    return fitness;
}


Point center2(Field &field, int P, Player *players, int B, int b, Point *patrons){
    lld best = -inf - 2, fit;
    Point bd;
    if ((fit = fitness2(field, P, players, B, b, patrons, STAND)) > best)
        best = fit, bd = STAND;
    if ((fit = fitness2(field, P, players, B, b, patrons, LEFT)) > best)
        best = fit, bd = LEFT;
    if ((fit = fitness2(field, P, players, B, b, patrons, RIGHT)) > best)
        best = fit, bd = RIGHT;
    if ((fit = fitness2(field, P, players, B, b, patrons, UP)) > best)
        best = fit, bd = UP;
    if ((fit = fitness2(field, P, players, B, b, patrons, DOWN)) > best)
        best = fit, bd = DOWN;
    return bd;
}

int filter_pat(int n, Point *ps, Field &t, Point I, int time){
    int st = 0;
    for (int i = 0; i < n; i++)
        if (dist(I, ps[i]) < t(ps[i]) - time)
            ps[st++] = ps[i];
    return st;

}


int main()
{
    //char str[100];
    //while (gets(str))
    //    cerr << str << endl;
    //return 0;
    scanf("%d", &N);
    Field field(N), dt(N);
    fc = Point((N + 2) / 2, (N + 1) / 2);
    armpos = Point(1, 0);
    armdir = 0;
    int t = 0;
    while (true){
        if (dt(armpos + ad[armdir]) != 0)
            armdir = (armdir + 1) & 3;
        armpos = armpos + ad[armdir];
        if (dt(armpos) != 0)
            break;
        dt(armpos) = ++t;
    }
    armpos = Point(1, 0);
    armdir = 0;
    t = 0;
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
        int b = filter_pat(B, patrons, dt, players[0].pos, -T);
        /*cerr << "SP:" << CC.x << " " << CC.y << endl;
        Point &I = players[0].pos;
        int tm = field(I);
        field(I) = 1;
        view_field(field);
        field(I) = tm;*/
        if (P > 2)
            printf("%s\n", dirtostr(center1(field, P, players, B, b, patrons)));
        else
            printf("%s\n", dirtostr(center2(field, P, players, B, b, patrons)));
        fflush(stdout);
    }
    return 0;
}
