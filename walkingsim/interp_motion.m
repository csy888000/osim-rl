xi=0:1/200:1;
x=normal(:,1);
normal_new = zeros(201,18);
for i = 1:18
    y=normal(:,i);
    yi=interp1(x,y,xi, 'spline');
    normal_new(:,i) = yi;
    if i == 2
        plot(x,y,'.' ,xi,yi,'o')
    end
    hold on
end

xlswrite("normal_new.xls", normal_new)