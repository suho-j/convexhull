datasource = 'MySQL64';
conn = database(datasource, 'kgm', '123123');

selectqueryX = 'SELECT RWRIST_X FROM rwrist_test3';
selectqueryY = 'SELECT RWRIST_Y FROM rwrist_test3';
selectqueryZ = 'SELECT RWRIST_Z FROM rwrist_test3';

dataX = select(conn,selectqueryX);
dataY = select(conn,selectqueryY);
dataZ = select(conn,selectqueryZ);
X = table2array(dataX)';
Y = table2array(dataY)';
Z = table2array(dataZ)';

x = double(X);
y = double(Y);
z = double(Z);
%P = [table2array(X)'; table2array(Y)'; table2array(Z)']' ;
P = [x; y; z]' ;
P = P*1;

figure('Name','Trace of the RWrist','NumberTitle','off');
plot3(P(:,1),P(:,2),P(:,3),'.','MarkerSize',10);
%title('Trace of the RWrist')
xlabel('x') % x-axis label
ylabel('y') % x-axis label
zlabel('z') % x-axis label
grid on

[k, vol] = boundary(P, 0.8);
hold on
trisurf(k,P(:,1),P(:,2),P(:,3),'Facecolor','red','FaceAlpha',0.1);
fprintf("vomlume: %d [m2]\n", vol)