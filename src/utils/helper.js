export const convertStringToJSON = (str) => {
  try {
    return JSON.parse(str);
  } catch (e) {
    return e;
  }
};

export const convertJSONToString = (json) => {
  try {
    return JSON.stringify(json);
  } catch (e) {
    return e;
  }
};

export const formatObjectToTitleCase = (obj) => {
  const formattedObj = {};

  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      let formattedKey;

      if (key.includes("_")) {
        // Convert underscore_case to Title Case with spaces
        formattedKey = key
          .split("_")
          .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
          .join(" ");
      } else {
        // Convert camelCase to Title Case with spaces
        formattedKey = key
          .replace(/([A-Z])/g, " $1") // Insert space before uppercase letters
          .replace(/^./, (str) => str.toUpperCase()); // Capitalize the first letter
      }

      formattedObj[key] = {
        originalKey: key,
        formattedKey: formattedKey,
        value: obj[key],
      };
    }
  }

  return formattedObj;
};
