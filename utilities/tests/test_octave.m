disp(['(Matlab or Octave) release R', version])
        
x = 0:.1:1000;
A = [x; sin(x/10.0)];

fileID = fopen('test_octave.dat','w');
fprintf(fileID,'%f\t%f\n',A);
fclose(fileID);

