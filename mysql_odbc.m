% datasource = 'MySQL64';
% conn = database(datasource, 'kgm', '123123');

datasource = 'MySQL64';
conn = database(datasource, 'kgm', '123123')


selectqueryX = 'SELECT RWRIST_X FROM rwrist_test3';
selectqueryY = 'SELECT RWRIST_X FROM rwrist_test3';
selectqueryZ = 'SELECT RWRIST_X FROM rwrist_test3';
dataX = select(conn,selectqueryX);
dataY = select(conn,selectqueryY);
dataZ = select(conn,selectqueryZ);

p = [table2array(dataX)'; table2array(dataY)'; table2array(dataZ)']'


% p = [];
% for i = 1:5
%     p(i) = dataX(i);
% end
% p
% %p = [dataX;dataY;dataZ]'
