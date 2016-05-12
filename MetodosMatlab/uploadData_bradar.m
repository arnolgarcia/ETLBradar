%% Definir directorio de trabajo

wkgdir = 'C:\Users\Arnol\Desktop\Datos Bradar\';

dir_coord = strcat(wkgdir,'geo_files\');
dir_data = strcat(wkgdir,'data_files\');


%% Generar archivo con las coordenadas del radar
% Archivo con las coordenadas del radar
file_coord = 'expXerem_radargeo';

% Crear directorio para los datos procesados si no existe si no existe.
if ~isdir(strcat(dir_coord,'processed'))
  disp(strcat('Warning: The following folder does not exist, so it was created: ', dir_coord));
  mkdir(strcat(dir_coord,'processed'));
end

% Cargar coordenada radar
fid_rad = fopen(strcat(dir_coord,file_coord),'r');
header_rad=fread(fid_rad,[1 8],'long');
vector_rad=fread(fid_rad,'double');
fclose(fid_rad);

% Guardar datos
dlmwrite(strcat(dir_coord,'processed\coordenadas_bradar.txt'),vector_rad,'delimiter','\t','precision',12);



%% Generar archivo con la data de las mediciones

% Archivos con las coordendas de cada punto
file_x = 'expXerem_eastinterp';
file_y = 'expXerem_northinterp';
file_z = 'expXerem_demcuttedinterp';

% Check to make sure that folder actually exists.  Warn user if it doesn't.
if ~isdir(dir_data)
  errorMessage = sprintf('Error: The following folder does not exist:\n%s', dir_data);
  uiwait(warndlg(errorMessage));
  return;
end

% Crear directorio para los datos procesados si no existe si no existe.
if ~isdir(strcat(dir_data,'processed'))
  disp(strcat('Warning: The following folder does not exist, so it was created: ', dir_data));
  mkdir(strcat(dir_data,'processed'));
end

% Cargar coordenada norte
fid_north = fopen(strcat(dir_coord,file_y),'r');
header_north=fread(fid_north,[1 8],'long');
vector_north=fread(fid_north,'double');
fclose(fid_north);
clear file_y fid_north;

% Cargar coordenada este
fid_east = fopen(strcat(dir_coord,file_x),'r');
header_east=fread(fid_east,[1 8],'long');
vector_east=fread(fid_east,'double');
fclose(fid_east);
clear file_x fid_east;

% Cargar coordenada altura
fid_z = fopen(strcat(dir_coord,file_z),'r');
header_z=fread(fid_z,[1 8],'long');
vector_z=fread(fid_z,'int16');
fclose(fid_z);
clear file_z fid_z;


% Get a list of all files in the folder with the desired file name pattern.
filePattern = fullfile(dir_data, '*expXerem*pha_ext_acumulada*'); % Patron para los datos de desplazamiento.
theFiles = dir(filePattern);
for k = 1 : length(theFiles)
  file_desp = theFiles(k).name;
  fecha = strcat(file_desp(10:13),'-',file_desp(14:15),'-',file_desp(16:17),'__',file_desp(19:26));
  
  % Cargar desplazamiento
  fid_desp = fopen(strcat(dir_data,file_desp),'r');
  header_desp=fread(fid_desp,[1 8],'long');
  vector_desp=fread(fid_desp,'double');
  fclose(fid_desp);

  % Guarda datos en un archivo
  %cabecera = ['este' 'norte' 'altura' 'deformacion'];
  datos=[vector_east vector_north vector_z vector_desp];
  dlmwrite(strcat(dir_data,'processed\','datos_bradar_',fecha,'.txt'),datos,'delimiter','\t','precision',9);
end
