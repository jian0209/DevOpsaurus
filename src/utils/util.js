import { LOG_STATUS, ROLES, STATUS } from "./constants";
import { formatObjectToTitleCase } from "./helper";
import moment from "moment";

export const generateColumn = (
  passedData = [],
  isLog = false,
  isSetting = false,
  isOperate = false,
  isRefresh = false,
) => {
  const columns = [];

  const data = passedData[0] || {};

  if (typeof data !== "object" || data.length === 0) {
    return columns;
  }

  const formattedData = formatObjectToTitleCase(data);
  for (const key in formattedData) {
    columns.push({
      name: key,
      required: true,
      label: formattedData[key].formattedKey,
      align: "left",
      field: (row) => row[key],
      format: (val) => {
        if (
          key.toLowerCase().includes("time") ||
          key.includes("createdAt") ||
          key.includes("updatedAt")
        ) {
          return `${moment(val).format("YYYY-MM-DD HH:mm:ss")}`;
        } else {
          return typeof val === "string" && val.length > 20
            ? `${val.substring(0, 20)}...`
            : isLog && key === "status"
              ? LOG_STATUS[val] || "Unknown"
              : isSetting && key.toLowerCase().includes("status")
                ? STATUS[val] || "Unknown"
                : key === "role"
                  ? ROLES[val]
                  : val;
        }
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
