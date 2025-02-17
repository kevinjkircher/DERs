%% introduction
% This script implements the gradient descent method for unconstrained
% differentiable optimization in a simple example.
%
% Kevin J. Kircher, Purdue University, 2025
%
% Please make sure the following file is on your Matlab path:
%   configureGraphics.m (configures graphics settings)

%% objective function and its gradient
% objective function
f = @(z) exp(z(1,:) + 3*z(2,:) - 0.1) + exp(z(1,:) - 3*z(2,:) - 0.1) + exp(-z(1,:) - 0.1);

% gradient of objective function
fGrad = @(z) ... 
    [ 1; % replace "1" with first component of gradient, similar to f = (z) ...
      2 ]; % replace "2" with second component of gradient

%% gradient descent implementation
% stopping conditions
K = 100; % maximum number of iterations
small = 1e-6; % stopping threshold for the norm of the gradient

% data storage
d = zeros(2,K); % descent directions
x = zeros(2,K+1); % iterates
alpha = zeros(1,K+1); % step sizes

% initialization
x(:,1) = [-2.5,0.5]; % initial guess
alpha(1) = 1; % initial step size

% solution
for k=1:K
    % descent direction
    % your code here
    
    % convergence check
    if % your code here
        break
    end
    
    % line search
    %
    % your
    % code
    % here
    % 
    
    % iterate update
    % your code here
end

% trim data storage for unreached iterations
fprintf('Gradient descent exited after %i iterations.\n',k)
if k < K
    d(:,k+1:K) = [];
    x(:,k+2:K) = [];
    alpha(k+2:K) = [];
    K = k;
end

%% plots
% function values
n = 1e3; % number of grid points in each dimension
x1 = linspace(-3,1,n);
x2 = linspace(-1,1,n);
[X1,X2] = meshgrid(x1,x2);
fPlot = zeros(n);
for i=1:n
    for j=1:n
        fPlot(i,j) = f([X1(i,j);X2(i,j)]);
    end
end

% contour plot
figure(1), clf
contour(X1,X2,fPlot,'showtext','on')
hold on
for k=1:K
    plot(x(1,k),x(2,k),'o','markersize',10)
    if k>1
        plot(x(1,k-1:k),x(2,k-1:k),'k--')
    end
end
xlabel('$x_1$')
ylabel('$x_2$')
axis square
xlim([min(x1),max(x1)])
ylim([min(x2),max(x2)])

% objective value plot
figure(2), clf
subplot(3,1,1), semilogy(f(x) - 2.559266696658216), grid on
ylabel('$f(x(k)) - f(x^\star)$')
xlim([1 K])
ylim([1e-16,1e1])
yticks([1e-16 1e-8 1e0])

% gradient norm plot
gradNorms = zeros(1,K);
for k=1:K
    gradNorms(k) = norm(fGrad(x(:,k)));
end
subplot(3,1,2), semilogy(1:K,gradNorms), grid on
ylabel('$\|\nabla f(x(k))\|$')
xlim([1 K])
ylim([1e-8,1e1])
yticks([1e-8 1e-4 1e0])

% step size plot
subplot(3,1,3), plot(alpha), grid on
ylabel('$\alpha(k)$')
xlabel('$k$')
ylim([0 1])
xlim([1 K])















