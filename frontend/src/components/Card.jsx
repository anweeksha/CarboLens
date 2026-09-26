const Card = ({ children, className = '', variant = 'default', ...props }) => {
  const baseStyles = 'rounded-lg border border-white/[0.08] bg-surface-container';
  
  const variants = {
    default: baseStyles,
    elevated: 'rounded-lg border border-white/[0.08] bg-surface-container-high shadow-lg',
    translucent: 'rounded-lg border border-white/[0.08] bg-surface-translucent-low/50 backdrop-blur-sm',
    ghost: 'rounded-lg border border-white/[0.08] bg-transparent',
  };

  return (
    <div className={`${variants[variant]} ${className}`} {...props}>
      {children}
    </div>
  );
};

export default Card;