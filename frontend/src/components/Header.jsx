function Header() {
  return (
    <header className="app-header">
      <div className="header-inner">
        <span className="header-wordmark">MOSHOFLO</span>
        <div className="header-right">
          <span className="header-title">Trade Dashboard</span>
          <div className="live-badge">
            <span className="live-dot" />
            LIVE
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
