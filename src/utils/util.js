import { LOG_STATUS, ROLES, STATUS } from "./constants";
import { formatObjectToTitleCase, formatTemplateVariables } from "./helper";
import moment from "moment";

export const generateColumn = (
  passedData = [],
  isLog = false,
  isSetting = false,
  isOperate = false,
  isRefresh = false,
  isDialog = false,
) => {
  const columns = [];

  const data = passedData[0] || {};

  if (typeof data !== "object" || data.length === 0) {
    return columns;
  }

  const formattedData = formatObjectToTitleCase(data);

  for (const key in formattedData) {
    if (key === "force_change_password") {
      continue;
    }
    columns.push({
      name: key,
      required: true,
      label: formattedData[key].formattedKey,
      align: "left",
      field: (row) => row[key],
      format: (val) => {
        if (isDialog) {
          return val;
        }
        if (
          key.toLowerCase().includes("time") ||
          key.includes("created_at") ||
          key.includes("updated_at")
        ) {
          return `${moment(val).format("YYYY-MM-DD HH:mm:ss")}`;
        }
        return typeof val === "string" && val.length > 40
          ? `${val.substring(0, 40)}...`
          : isLog && key === "status"
            ? LOG_STATUS[val] || "Unknown"
            : isSetting && key.toLowerCase().includes("status")
              ? STATUS[val] || "Unknown"
              : key === "role"
                ? ROLES[val]
                : val;
      },
      sortable: true,
    });
  }
  if (isOperate) {
    columns.push({
      name: "operate",
      field: "operate",
      label: "Operate",
      align: "right",
      sortable: false,
    });
  }
  if (isRefresh) {
    columns.push({
      name: "refresh",
      field: "refresh",
      label: "",
      align: "center",
      sortable: false,
    });
  }
  return columns;
};

export const generateSearchForm = (passedData = "") => {
  return formatTemplateVariables(passedData);
};

export const generateDialogDetails = (passedData = {}) => {
  return formatObjectToTitleCase(passedData);
};

export const replaceCommandString = (str, obj) => {
  return str.replace(/{([^{}]*)}/g, (a, b) => {
    let r = obj[b];
    return typeof r === "string" || typeof r === "number" ? r : a;
  });
};

export const replaceQueryString = (str, obj) => {
  return str.replace(/{([^{}]*)}/g, (a, b) => {
    let r = obj[b];
    console.log(r);
    if (r.includes(",")) {
      return r
        .split(",")
        .map((item) => {
          return typeof item === "string" || typeof item === "number"
            ? `'${item}'`
            : a;
        })
        .join(",");
    }
    return typeof r === "string" || typeof r === "number" ? `'${r}'` : a;
  });
};

export const generateModifyForm = () => {
  return { label: "Value", model: "value", type: "text" };
};

export const generateColumnFromString = (passedData = "") => {};

export const wrapCsvValue = (val, formatFn, row) => {
  let formatted = formatFn !== void 0 ? formatFn(val, row) : val;

  formatted =
    formatted === void 0 || formatted === null ? "" : String(formatted);

  formatted = formatted.split('"').join('""');
  /**
   * Excel accepts \n and \r in strings, but some other CSV parsers do not
   * Uncomment the next two lines to escape new lines
   */
  // .split('\n').join('\\n')
  // .split('\r').join('\\r')

  return `"${formatted}"`;
};
