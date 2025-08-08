// frontend/src/components/QrScanner.tsx
import React from 'react';
import { QrReader } from 'react-qr-reader';

interface QrScannerProps {
  onResult: (result: string) => void;
  onError: (error: any) => void;
}

const QrScanner: React.FC<QrScannerProps> = ({ onResult, onError }) => (
  <QrReader
    constraints={{ facingMode: 'environment' }}
    scanDelay={300}
    onResult={(result, error) => {
      if (!!result) {
        onResult(result.getText());
      }
      if (!!error) {
        onError(error);
      }
    }}
    style={{ width: '100%' }}
  />
);

export default QrScanner;
