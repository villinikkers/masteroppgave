% Input: power spectrum density values calculated by the eeglab function
% spectopo(). These values are given in units of 10*log10(uV^2/Hz)
% format of the specData matrix is: [channels x frequency]
% 
% - Output: 
%   - bandPowerAbs = [freqBand x channel]
%   - tots = total power in each channel
%
function [bandPowerAbs, bandPowerdB, tots] = calcBandpowers2(specData)
    % The frequencyBands denotes the indexes for the frequencies
    % in the specified frequency band. Since matlab is 1-indexed
    % range [1:4] corresponds to frequency 0-3 Hz (3 inclusive).
    frequencyBands = struct(...
        'delta', [1:4],...
        'theta', [5:8],...
        'alpha', [9:13],...
        'beta', [14:31],...
        'gamma', [32:101]);
    
    % Convert to specData from 10*log(uV^2/Hz) to absolute values (uV^2/Hz):
    % define pure function that applies the transformation: 
    % y = 10^(x/10) elementwise on the input x.
    f = @(x)arrayfun(@(x2)10^(x2/10),x); 
    
    % Function to convert from uV^2 back to 10*log(uV^2/Hz):
    f2 = @(x)arrayfun(@(x2)10*log10(x2),x);
    
    specDataAbs = f(specData);
    tots = sum(specDataAbs(:,1:101),2);
    % preallocate the bandPowerAbs matrix:
    bandPowerAbs = zeros(size(specData,1), length(fieldnames(frequencyBands)));
    bandPowerdB = bandPowerAbs; %Preallocate variable for log spectral density
    
    for i=1:size(specDataAbs,1)
        % Calculate absolute spectral power in uV^2
        bandPowerAbs(i,:) = [...
            sum(specDataAbs(i, frequencyBands.delta)),...
            sum(specDataAbs(i, frequencyBands.theta)),...
            sum(specDataAbs(i, frequencyBands.alpha)),...
            sum(specDataAbs(i, frequencyBands.beta)),...
            sum(specDataAbs(i, frequencyBands.gamma))];
        
    end
    
    bandPowerdB = f2(bandPowerAbs);
    
    
    
end