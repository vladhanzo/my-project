// frontend/src/components/QrLabel.tsx
import React from 'react';

interface QrLabelProps {
  url: string;
  alt?: string;
}

const QrLabel: React.FC<QrLabelProps> = ({ url, alt = 'QR Code' }) => (
  <img src={url} alt={alt} style={{ maxWidth: '100%', height: 'auto' }} />
);

export default QrLabel;
