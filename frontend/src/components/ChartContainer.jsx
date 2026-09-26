import Card from './Card';

const ChartContainer = ({ title, children, actions, className = '' }) => {
  return (
    <Card className={`p-6 ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="font-headline-md text-headline-md font-medium text-primary">
            {title}
          </h3>
          <div className="h-1 w-12 bg-gradient-to-r from-primary to-primary/20 rounded-full mt-2" />
        </div>
        
        {actions && (
          <div className="flex items-center gap-2">
            {actions}
          </div>
        )}
      </div>
      
      <div className="h-64">
        {children}
      </div>
      
      <div className="flex items-center justify-between mt-4 pt-4 border-t border-white/[0.08]">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="h-2 w-4 bg-gradient-to-r from-primary to-primary/50 rounded-sm" />
            <span className="text-xs text-on-surface-variant">Current</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-2 w-4 bg-gradient-to-r from-on-surface-variant to-on-surface-variant/50 rounded-sm" />
            <span className="text-xs text-on-surface-variant">Previous</span>
          </div>
        </div>
        
        <button className="text-xs text-on-surface-variant hover:text-primary transition-colors">
          View details →
        </button>
      </div>
    </Card>
  );
};

export default ChartContainer;