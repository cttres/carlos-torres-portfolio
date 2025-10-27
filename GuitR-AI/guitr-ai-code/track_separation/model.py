import torch
import torch.nn as nn

class ChordRNN(nn.Module):
    def __init__(self, input_size=12, hidden_size=64, num_layers=2, num_classes=10):
        super(ChordRNN, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        # x shape: (batch_size, seq_length, input_size)
        out, _ = self.lstm(x)
        # We take the last time step's output for classification
        out = out[:, -1, :]
        out = self.fc(out)
        return out
