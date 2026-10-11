'use client';

import React, { useState } from 'react';
import { 
  Clock, 
  CheckCircle, 
  Flag, 
  CloudRain
} from 'lucide-react';
import { ConstructionSchedule, ScheduleTask } from '@/lib/types';
import { updateScheduleTaskApi } from '@/lib/api';

interface GanttScheduleChartProps {
  schedule: ConstructionSchedule;
}

export default function GanttScheduleChart({ schedule }: GanttScheduleChartProps) {
  const [tasks, setTasks] = useState<ScheduleTask[]>(schedule.tasks || []);
  const maxDays = schedule.total_duration_days || 220;

  const handleToggleTaskStatus = async (task: ScheduleTask) => {
    const nextStatus = task.status === 'Completed' ? 'In Progress' : task.status === 'In Progress' ? 'Completed' : 'In Progress';
    const updated = tasks.map((t) => t.id === task.id ? { ...t, status: nextStatus } : t);
    setTasks(updated);

    if (schedule.id) {
      try {
        await updateScheduleTaskApi(schedule.id, task.id, { status: nextStatus });
      } catch (err) {
        console.error('Failed to update task status:', err);
      }
    }
  };

  return (
    <div className="space-y-6">
      {/* Schedule Summary Banner */}
      <div className="bg-white border border-slate-200 shadow-sm p-5 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="p-1.5 rounded-lg bg-blue-50 text-blue-600 border border-blue-200">
              <Clock className="w-4 h-4" />
            </span>
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
              Critical Path Construction Schedule (CPM)
            </h3>
          </div>
          <p className="text-xs text-slate-600">
            Total Duration: <span className="text-blue-700 font-bold">{schedule.total_duration_days} Days</span> (~{schedule.total_months} Months) | 
            Commencement: <span className="text-slate-900 font-semibold">{schedule.commencement_date}</span> ➔ 
            Handover: <span className="text-blue-700 font-bold">{schedule.estimated_completion_date}</span>
          </p>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <div className="px-3 py-1.5 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-xs font-semibold flex items-center gap-1.5">
            <CloudRain className="w-4 h-4 text-amber-600" />
            <span>Monsoon Buffer Added</span>
          </div>
        </div>
      </div>

      {/* Gantt Timeline View */}
      <div className="bg-white border border-slate-200 shadow-sm rounded-2xl overflow-hidden">
        <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <span className="text-xs font-bold text-slate-900 uppercase tracking-wider">
            Phases & Task Dependencies
          </span>
          <div className="flex items-center gap-4 text-[11px] text-slate-600">
            <span className="flex items-center gap-1.5 font-medium">
              <span className="w-3 h-2 rounded bg-amber-500" />
              Critical Path
            </span>
            <span className="flex items-center gap-1.5 font-medium">
              <span className="w-3 h-2 rounded bg-blue-600" />
              Standard Task
            </span>
            <span className="flex items-center gap-1.5 font-medium">
              <Flag className="w-3 h-3 text-blue-600" />
              Milestone Gate
            </span>
          </div>
        </div>

        <div className="divide-y divide-slate-100 p-4 space-y-4">
          {tasks.map((task) => {
            const leftPercent = (task.start_day / maxDays) * 100;
            const widthPercent = Math.max((task.duration_days / maxDays) * 100, 3);

            return (
              <div key={task.id} className="pt-3 first:pt-0">
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleToggleTaskStatus(task)}
                      className={`p-0.5 rounded transition ${
                        task.status === 'Completed'
                          ? 'text-emerald-600 hover:text-emerald-700'
                          : 'text-slate-400 hover:text-slate-600'
                      }`}
                      title="Click to toggle status"
                    >
                      <CheckCircle className="w-4 h-4" />
                    </button>
                    <span className="font-semibold text-slate-900">
                      {task.task_name}
                    </span>
                    {task.milestone && (
                      <span className="px-1.5 py-0.5 rounded text-[10px] bg-blue-50 text-blue-700 border border-blue-200 flex items-center gap-1 font-semibold">
                        <Flag className="w-2.5 h-2.5" /> Milestone
                      </span>
                    )}
                    {task.is_critical && (
                      <span className="px-1.5 py-0.5 rounded text-[10px] bg-amber-50 text-amber-800 border border-amber-200 font-semibold">
                        Critical
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-3 text-slate-500 font-mono text-[11px]">
                    <span>Day {task.start_day} - {task.end_day}</span>
                    <span className="text-blue-700 font-bold">{task.duration_days}d</span>
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-sans font-semibold ${
                        task.status === 'Completed'
                          ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                          : task.status === 'In Progress'
                          ? 'bg-blue-50 text-blue-700 border border-blue-200'
                          : 'bg-slate-100 text-slate-600'
                      }`}
                    >
                      {task.status}
                    </span>
                  </div>
                </div>

                {/* Gantt Bar Background & Fill */}
                <div className="w-full h-3 rounded-full bg-slate-100 overflow-hidden relative border border-slate-200">
                  <div
                    className={`h-full rounded-full transition-all duration-300 ${
                      task.is_critical
                        ? 'bg-gradient-to-r from-amber-500 to-orange-500 shadow-xs'
                        : 'bg-blue-600'
                    }`}
                    style={{
                      marginLeft: `${leftPercent}%`,
                      width: `${widthPercent}%`
                    }}
                  />
                </div>

                {task.description && (
                  <p className="text-[11px] text-slate-500 mt-1 pl-6">
                    {task.description}
                  </p>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
