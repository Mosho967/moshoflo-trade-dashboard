import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function Header() {
  return (
    <div className="text-center my-4">
      <img
        src="/images/moshoflo_logo.png"
        alt="Moshoflo Logo"
        style={{ maxHeight: '150px' }}
        className="mb-2"
      />
      <h2 className="mt-3">Trade Overview</h2>
    </div>
  );
}

export default Header;