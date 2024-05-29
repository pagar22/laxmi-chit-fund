export const formatDate = (date) => {
  return new Date(date || Date.now()).toISOString().split("T")[0];
};

export const rounded = (value, decimals = 2) => {
  const base = Math.pow(10, decimals);
  return Math.round(value * base) / base;
};

export const camelToTitle = (camelCase) => {
  return camelCase
    .replace(/([A-Z])/g, " $1")
    .replace(/^./, (str) => str.toUpperCase());
};