import type { ReactNode } from "react";
import { useSelector } from "react-redux";
import { selectIsAthenticated } from "../features/auth/authSlice";
import { Navigate } from "react-router";

const ProtectedRoute = ({ children }: { children: ReactNode }) => {
  const isAuth = useSelector(selectIsAthenticated);

  if (!isAuth) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
