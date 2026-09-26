const Metric = ({ label, value, unit, trend, description, className = '' }) => {
  return (
    <div className={`flex flex-col ${className}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="font-eyebrow-tag text-eyebrow-tag text-on-surface-variant uppercase tracking-wider">
          {label}
        </span>
        {trend && (
          <span className={`text-xs font-medium ${trend.value > 0 ? 'text-error' : 'text-primary'}`}>
            {trend.value > 0 ? '↑' : '↓'} {Math.abs(trend.value)}%
          </span>
        )}
      </div>
      
      <div className="flex items-baseline gap-2">
        <span className="font-metric-large text-metric-large font-semibold text-primary tracking-tight">
          {value}
        </span>
        {unit && (
          <span className="font-body-md text-body-md text-on-surface-variant">
            {unit}
          </span>
        )}
      </div>
      
      {description && (
        <p className="mt-2 font-body-sm text-body-sm text-on-surface-variant">
          {description}
        </p>
      )}
    </div>
  );
};

export default Metric;