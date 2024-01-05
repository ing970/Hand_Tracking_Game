import torch
import torch.nn as nn

# 모델 아키텍처 정의
class HandStateNN(nn.Module):
    def __init__(self, n_classes):
        super(HandStateNN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(63, 256), 
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.5),
            
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(0.5),
            
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.5),
            
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Dropout(0.5),
            
            nn.Linear(128, 64),
            nn.ReLU(),
            
            nn.Linear(64, n_classes)
        )
    def forward(self, x):
        return self.network(x)
    
model = HandStateNN(n_classes=5)  
model.load_state_dict(torch.load('./model/best_model.pth'))
model.eval()
