program mybot;
    var move: string;
    var n, p, b, k: longint;
    var x, y, b0, x1, y1, b1: longint;
    var bullets: array [1..1000, 1..2] of longint;
    var i, xb, yb, min: longint;
    
function todot(y, x, y1, x1: longint): string;
begin
    if (x < x1) then move := 'RIGHT'   
    else if (x > x1) then move := 'LEFT'
    else if (y < y1) then move := 'DOWN'
    else if (y > y1) then move := 'UP'
    else move := 'STAND'; 
    todot := move;
end;
begin
    readln(n);
    
    while True do
    begin
        readln(p, b, k);
        readln(x, y, b0);
        readln(x1, y1, b1);
        for i := 1 to b do
        begin
            readln(bullets[i][1], bullets[i][2]);
        end;
        if (k < 0) then
        begin
            move := todot(x, y, n div 2, n div 2);
        end
        else
        if (b = 0) then
        begin
            move := todot(x, y, x1, y1)
        end
        else
        begin
            min := abs(x - bullets[1][1]) + abs(y - bullets[1][2]);
            xb := bullets[1][1];
            yb := bullets[1][2];
            for i := 1 to b do
            begin
                if (abs(x - bullets[i][1]) + abs(y - bullets[i][2]) < min) then
                begin
                    min := abs(x - bullets[i][1]) + abs(y - bullets[i][2]);
                    xb := bullets[i][1];
                    yb := bullets[i][2];
                end;
            end;
            move := todot(x, y, xb, yb);
        end;
        writeln(move);
        flush(output);
    end;
end.
