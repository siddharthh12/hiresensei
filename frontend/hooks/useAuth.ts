import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';

export function useAuth() {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(true);
    const router = useRouter();

    useEffect(() => {
        const token = Cookies.get('token');
        if (token) {
            setIsAuthenticated(true);
        } else {
            setIsAuthenticated(false);
        }
        setLoading(false);
    }, []);

    const login = (token: string) => {
        Cookies.set('token', token, { expires: 7 }); // Expires in 7 days
        localStorage.setItem('token', token); // Keep localStorage for existing API calls if needed
        setIsAuthenticated(true);
        router.push('/dashboard');
    };

    const logout = () => {
        Cookies.remove('token');
        localStorage.removeItem('token');
        setIsAuthenticated(false);
        router.push('/login');
    };

    return { isAuthenticated, loading, login, logout };
}
