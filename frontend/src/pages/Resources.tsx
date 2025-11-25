import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import Layout from '@/components/Layout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { 
  ArrowLeft, 
  Server, 
  Globe, 
  Link2, 
  Database, 
  HardDrive, 
  Network,
  Key,
  Box,
  FolderOpen,
  MapPin,
  Calendar,
  Activity,
  Cloud,
  Shield,
  Zap,
  Cpu,
  Boxes,
  Container,
  Folder,
  Lock
} from 'lucide-react';
import { api } from '@/lib/api';

interface Resource {
  id: number;
  icon: string;
  title: string;
  resource_name: string;
  description: string;
  status: string;
  region: string;
  created_at: string;
}

// Icon mapping
const iconMap: Record<string, any> = {
  server: Server,
  globe: Globe,
  link: Link2,
  database: Database,
  hard_drive: HardDrive,
  network: Network,
  key: Key,
  box: Box,
  folder_open: FolderOpen,
  cloud: Cloud,
  shield: Shield,
  zap: Zap,
  activity: Activity,
  cpu: Cpu,
  boxes: Boxes,
  container: Container,
  folder: Folder,
  lock: Lock,
};

export default function Resources() {
  const navigate = useNavigate();
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Fetch resources from API
  const { data: resources = [], isLoading } = useQuery<Resource[]>({
    queryKey: ['resources'],
    queryFn: async () => {
      const response = await api.getResources();
      return response || [];
    },
  });

  const handleResourceClick = (resource: Resource) => {
    setSelectedResource(resource);
    setIsModalOpen(true);
  };

  const getStatusColor = (status: string) => {
    const statusLower = status?.toLowerCase() || '';
    if (statusLower.includes('run')) return 'bg-green-500';
    if (statusLower.includes('stop')) return 'bg-red-500';
    if (statusLower.includes('pend')) return 'bg-yellow-500';
    return 'bg-gray-500';
  };

  const getIconComponent = (iconName: string) => {
    return iconMap[iconName] || Server;
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="p-6 max-w-7xl mx-auto">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary" />
              <p className="mt-4 text-muted-foreground">Loading resources...</p>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="p-4 sm:p-6 max-w-7xl mx-auto">
        <div className="mb-6 sm:mb-8 flex items-center gap-3 sm:gap-4">
          <Button
            variant="outline"
            size="icon"
            onClick={() => navigate('/')}
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold">Your Resources</h1>
            <p className="text-sm sm:text-base text-muted-foreground mt-1">
              Manage and monitor your infrastructure
            </p>
          </div>
        </div>

        {resources.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-muted-foreground mb-4">
                No resources found. Add resources from the Settings page.
              </p>
              <Button onClick={() => navigate('/settings')}>
                Go to Settings
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {resources.map((resource) => {
              const IconComponent = getIconComponent(resource.icon);
              return (
                <Card
                  key={resource.id}
                  className="cursor-pointer transition-all duration-300 hover:shadow-xl hover:scale-105 bg-gradient-to-br from-blue-50/50 to-indigo-50/50 dark:from-blue-950/20 dark:to-indigo-950/20 border-blue-100 dark:border-blue-900/50"
                  onClick={() => handleResourceClick(resource)}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-3">
                      <div className="p-3 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-500 shadow-lg">
                        <IconComponent className="h-5 w-5 text-white" strokeWidth={2.5} />
                      </div>
                      <div className="flex-1">
                        <CardTitle className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                          {resource.title}
                        </CardTitle>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <h3 className="text-xl font-bold text-blue-600 dark:text-blue-400 mb-2 truncate">
                      {resource.resource_name}
                    </h3>
                    <CardDescription className="mb-4 line-clamp-2 text-sm">
                      {resource.description}
                    </CardDescription>
                    <p className="text-xs text-blue-600 dark:text-blue-400 font-medium flex items-center gap-1">
                      Click to view details 
                      <span className="text-base">→</span>
                    </p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}

        {/* Resource Detail Modal */}
        <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
          <DialogContent className="max-w-2xl w-[calc(100%-1.5rem)] sm:w-auto sm:max-h-[90vh] sm:overflow-y-auto bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900 border-0 shadow-2xl p-4 sm:p-6">
            {selectedResource && (
              <>
                <DialogHeader className="border-b pb-1.5 sm:pb-3 space-y-1">
                  <DialogTitle className="text-xl font-bold text-green-600 dark:text-green-400">
                    {selectedResource.title}
                  </DialogTitle>
                </DialogHeader>

                <div className="space-y-1.5 sm:space-y-3 py-1.5 sm:py-3">
                  <div className="p-2 sm:p-3 rounded-lg bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm">
                    <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                      Resource Name
                    </label>
                    <p className="text-sm sm:text-base font-bold mt-1 text-foreground break-words">
                      {selectedResource.resource_name}
                    </p>
                  </div>

                  <div className="p-2 sm:p-3 rounded-lg bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm">
                    <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                      Description
                    </label>
                    <p className="text-xs sm:text-sm mt-1 text-foreground">
                      {selectedResource.description}
                    </p>
                  </div>

                  <div className="flex items-center gap-2 p-2 sm:p-3 rounded-lg bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm">
                    <div className={`w-2 h-2 rounded-full ${getStatusColor(selectedResource.status)}`} />
                    <span className="text-green-600 dark:text-green-400 font-semibold text-xs sm:text-sm">
                      {selectedResource.status}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
                    <div className="p-2 sm:p-3 rounded-lg bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm flex items-center gap-2">
                      <div className="p-1.5 rounded-lg bg-blue-100 dark:bg-blue-900">
                        <MapPin className="h-3 w-3 sm:h-4 sm:w-4 text-blue-600 dark:text-blue-400" />
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground font-semibold">Region</p>
                        <p className="font-semibold text-xs sm:text-sm text-foreground">{selectedResource.region || 'East US'}</p>
                      </div>
                    </div>
                    <div className="p-2 sm:p-3 rounded-lg bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm flex items-center gap-2">
                      <div className="p-1.5 rounded-lg bg-purple-100 dark:bg-purple-900">
                        <Calendar className="h-3 w-3 sm:h-4 sm:w-4 text-purple-600 dark:text-purple-400" />
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground font-semibold">Created</p>
                        <p className="font-semibold text-xs sm:text-sm text-foreground">
                          {selectedResource.created_at ? new Date(selectedResource.created_at).toLocaleDateString() : new Date().toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="border-t pt-1.5 sm:pt-3">
                    <div className="flex items-center gap-2 mb-1.5 sm:mb-3">
                      <div className="p-1.5 rounded-lg bg-green-100 dark:bg-green-900">
                        <Activity className="h-3 w-3 sm:h-4 sm:w-4 text-green-600 dark:text-green-400" />
                      </div>
                      <h3 className="text-sm sm:text-base font-bold">Performance Metrics</h3>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-3">
                      <div className="text-center p-2 sm:p-3 rounded-lg bg-gradient-to-br from-green-50 to-emerald-100 dark:from-green-950 dark:to-emerald-900 shadow-md">
                        <p className="text-xl sm:text-2xl font-bold text-green-600 dark:text-green-400">99.9%</p>
                        <p className="text-xs text-muted-foreground mt-1 font-semibold">Uptime</p>
                      </div>
                      <div className="text-center p-2 sm:p-3 rounded-lg bg-gradient-to-br from-blue-50 to-cyan-100 dark:from-blue-950 dark:to-cyan-900 shadow-md">
                        <p className="text-xl sm:text-2xl font-bold text-blue-600 dark:text-blue-400">45ms</p>
                        <p className="text-xs text-muted-foreground mt-1 font-semibold">Latency</p>
                      </div>
                      <div className="text-center p-2 sm:p-3 rounded-lg bg-gradient-to-br from-purple-50 to-pink-100 dark:from-purple-950 dark:to-pink-900 shadow-md">
                        <p className="text-xl sm:text-2xl font-bold text-purple-600 dark:text-purple-400">4.8/5</p>
                        <p className="text-xs text-muted-foreground mt-1 font-semibold">Health</p>
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </Layout>
  );
}
