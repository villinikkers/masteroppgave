function fig = plotSpectrogram3(EEG, titleString)
    baseTitleString = "Frequency power spectrum ";
    recordingLength = length(EEG.times);
    nChannels = length(EEG.chanlocs);
    channelLabels = [];
    for i=1:nChannels
        channelLabels = [channelLabels, string(EEG.chanlocs(i).labels)];
    end
    fig = figure; pop_spectopo(EEG, 1, [0      recordingLength],...
        'EEG' , 'freq', [7.81, 15.62, 23.43, 31.24, 39.05, 46.86],...
        'freqrange',[1 50],'electrodes','off');
    if nargin<2
        title(fig.Children(end), [baseTitleString]);
    else
        title(fig.Children(end), [baseTitleString titleString]);
    end
    legend(fig.Children(end-1),channelLabels); 
    
end