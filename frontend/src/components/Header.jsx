const STATUS_CONFIG = {
  live:        { label: "LIVE",       cls: "live-badge--live" },
  connecting:  { label: "CONNECTING", cls: "live-badge--connecting" },
  offline:     { label: "OFFLINE",    cls: "live-badge--offline" },
};

function Header({ wsStatus = "connecting" }) {
  const { label, cls } = STATUS_CONFIG[wsStatus] ?? STATUS_CONFIG.connecting;

  return (
    <header className="app-header">
      <div className="header-inner">
        <span className="header-wordmark">MOSHOFLO</span>
        <div className="header-right">
          <span className="header-title">Trade Dashboard</span>
          <div className={`live-badge ${cls}`}>
            <span className="live-dot" />
            {label}
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
