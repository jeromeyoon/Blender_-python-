clear all ;
close all ;

D = load('depth_shoe.mat');
D = D.zimage; 
D = D(:,1:end-1);
% imagesc(D)
mask = ones(size(D));
mask(D>100) = 0;
figure(),imshow(mask);
se = strel('disk',3);        
mask = imerode(mask,se);
mask = repmat(mask,[1,1,3]);
figure(),imshow(mask);

figure(),D(D>100) = 0;

grid = logical(ones(size(D)));
K = [1.462857177734375000e+03 0.000000000000000000e+00 2.560000000000000000e+02
0.000000000000000000e+00 1.462857177734375000e+03 2.560000000000000000e+02
0.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00  ];

vertex = genVertex (D,grid,K);
V = reshape(vertex,[3,size(D,1),size(D,1)]);
X = squeeze(V(1,:,:));
Y = squeeze(V(2,:,:));
Z = squeeze(V(3,:,:));

[nx,ny,nz] = surfnorm(X,Y,Z);
N = reshape([-nx ny nz], size(nx,1), size(nx,2),3); %range [-1,1]
N = N.*mask;
N = (N+1)./2;
figure(),imshow(N);

im = imread('normal_LF0_Cam004 (1).png');
S = im2double(im);
% figure(2),imshow(im);

% imagesc(D)

